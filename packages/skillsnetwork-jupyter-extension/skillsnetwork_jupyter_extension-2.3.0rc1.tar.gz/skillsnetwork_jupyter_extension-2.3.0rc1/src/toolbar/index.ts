import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { Dialog, showDialog, ToolbarButton } from '@jupyterlab/apputils';
import {
  getFileContents,
  getAuthorLabFilePath,
  openLab,
  openLearnerLab
} from '../tools';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import {
  atlasAxiosHandler,
  postAtlasLabModel,
  awbAxiosHandler,
  postAwbLabModel
} from '../handler';
import { showFailureImportLabDialog } from '../dialog';
import { Globals, EnvType, Mode, ENV_TYPE, FILE_PATH } from '../config';
import {
  ATLAS_TOKEN,
  AWB_TOKEN,
  SET_DEFAULT_LAB_NAME_AND_KERNEL,
  MODE,
  NOTEBOOK_URL
} from '../config';
import jwt_decode from 'jwt-decode';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  NotebookPanel,
  INotebookModel,
  INotebookTracker
} from '@jupyterlab/notebook';

import { SkillsNetworkFileLibrary } from '../sn-file-library';
import { PathExt } from '@jupyterlab/coreutils';

/**
 * The plugin registration information.
 */
const toolbar: JupyterFrontEndPlugin<void> = {
  id: 'skillsnetwork_jupyter_extension:toolbar',
  description: 'Toolbar plugin for Skills Network Authoring Extension',
  autoStart: true,
  requires: [INotebookTracker, IDocumentManager, IDefaultFileBrowser],
  activate
};

/**
 * Clean up workspace by closing all opened widgets
 */
async function cleanUpEnvironment(
  notebookTracker: INotebookTracker
): Promise<void> {
  notebookTracker.forEach(notebookPanel => {
    notebookPanel.dispose();
  });
}

/**
 * A notebook widget extension that adds buttons to the toolbar.
 */
export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    if (Globals.SHOW_PUBLISH_BUTTON_FOR !== context.path) {
      // This is not a Skills Network Lab notebook so return a no-op disposable
      return new DisposableDelegate(() => {});
    } else {
      // This is a Skills Network Lab notebook so add the publish button
      const publish = async () => {
        // POST to Atlas the file contents/lab model
        const fullPath: string = context.path;
        const token = Globals.TOKENS.get(fullPath);
        if (token === undefined) {
          console.log(
            `[ButtonExtension] No token found for filename: ${fullPath}`
          );
          await showDialog({
            title: 'Publishing Restricted',
            body: `Only the lab '${
              Globals.TOKENS.keys().next().value
            }' can be published during this editing session.`,
            buttons: [Dialog.okButton({ label: 'Dismiss' })]
          });
          return;
        }

        const token_info = jwt_decode(token) as { [key: string]: any };

        if ('version_id' in token_info) {
          await postAwbLabModel(awbAxiosHandler(token), panel, context, token);
        } else {
          await postAtlasLabModel(atlasAxiosHandler(token), panel, context);
        }
      };

      const download = async () => {
        const file = await getFileContents(panel, context);
        const blob = new Blob([file], { type: 'application/x-ipynb+json' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.setAttribute('download', PathExt.basename(context.path));
        link.setAttribute('href', url);

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      };

      const downloadButton = new ToolbarButton({
        className: 'download-lab-button',
        label: 'Download Notebook',
        onClick: download,
        tooltip: 'Download the current notebook ipynb file to your local system'
      });

      const publishButton = new ToolbarButton({
        className: 'publish-lab-button',
        label: 'Publish on SN',
        onClick: publish,
        tooltip: 'Publish Lab'
      });

      const snFileLibraryButton = new ToolbarButton({
        className: 'sn-file-library-button',
        label: 'SN File Library',
        onClick: () => new SkillsNetworkFileLibrary(context.path).launch(),
        tooltip: 'Skills Network File Library'
      });

      panel.toolbar.insertItem(8, 'download', downloadButton);
      panel.toolbar.insertItem(9, 'sn-file-library', snFileLibraryButton);
      panel.toolbar.insertItem(10, 'publish', publishButton);
      return new DisposableDelegate(() => {
        downloadButton.dispose();
        publishButton.dispose();
        snFileLibraryButton.dispose();
      });
    }
  }
}

/**
 * Activate the extension.
 *
 * @param app Main application object
 */
async function activate(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker,
  docManager: IDocumentManager,
  fileBrowser: IDefaultFileBrowser
) {
  console.log('Activating skillsnetwork_jupyter_extension button plugin!');

  const env_type = await SET_DEFAULT_LAB_NAME_AND_KERNEL();
  console.log('Using default kernel:', Globals.PY_KERNEL_NAME);

  if (MODE === Mode.LEARN) {
    if (ENV_TYPE !== EnvType.JUPYTERLITE) {
      return;
    }

    console.log('skillsnetwork_jupyter_extension:toolbar extension activated');

    if (NOTEBOOK_URL) {
      await app.serviceManager.ready;
      app.restored.then(async () => {
        await cleanUpEnvironment(notebookTracker);
        try {
          await openLearnerLab(
            NOTEBOOK_URL as string,
            FILE_PATH,
            docManager,
            app.serviceManager.contents,
            fileBrowser
          );
        } catch (e) {
          console.error('Error opening lab:', e);
          Dialog.flush(); // remove spinner
          showFailureImportLabDialog();
        }
      });
    } else {
      // No notebook URL found, so we can't load a notebook. This is not an error, so we don't need to show a dialog.
      console.log('No valid notebook URL found...');
    }
    return;
  }

  const atlas_token = ATLAS_TOKEN as string;
  const awb_token = AWB_TOKEN as string;

  console.log('skillsnetwork_jupyter_extension:toolbar extension activated');

  // Only show toolbar buttons for the lab that's launched via token
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());

  let dirPath = '';

  if (FILE_PATH !== null) {
    dirPath = getAuthorLabFilePath(FILE_PATH);
    console.log('Authoring lab file path:', dirPath);
  }

  // Try to load up a notebook when author is using the browser tool (not in local)
  await app.serviceManager.ready;
  app.restored.then(async () => {
    await cleanUpEnvironment(notebookTracker);
    if (
      env_type !== EnvType.LOCAL &&
      (atlas_token !== 'NO_TOKEN' || awb_token !== 'NO_TOKEN')
    ) {
      try {
        await openLab(
          atlas_token,
          awb_token,
          dirPath,
          docManager,
          app.serviceManager.contents,
          fileBrowser
        );
      } catch (e) {
        console.error('Error opening lab with Atlas/AWB token:', e);
        Dialog.flush(); // remove spinner
        showFailureImportLabDialog();
      }
    }
  });
}

/**
 * Export the plugin as default.
 */
export default toolbar;
