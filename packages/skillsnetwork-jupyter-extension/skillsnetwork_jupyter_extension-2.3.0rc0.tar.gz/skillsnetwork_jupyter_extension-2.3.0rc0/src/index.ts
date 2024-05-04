import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import menu from './menu';
import toolbar from './toolbar';
import theme from './theme';

console.log(
  'Initializing JupyterFrontEnd plugins for skillsnetwork_jupyter_extension.'
);

const main: JupyterFrontEndPlugin<any>[] = [menu, toolbar, theme];

console.log(
  'JupyterFrontEnd plugins defined:',
  main.map(p => p.id)
);

export default main;
