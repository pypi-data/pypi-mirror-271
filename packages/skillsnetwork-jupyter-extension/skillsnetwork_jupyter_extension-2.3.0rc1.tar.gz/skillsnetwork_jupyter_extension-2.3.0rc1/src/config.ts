import { ServerConnection } from '@jupyterlab/services';
import { KernelSpecAPI } from '@jupyterlab/services';

interface IConfiguration {
  ATLAS_BASE_URL: string;
  SN_FILE_LIBRARY_URL: string;
  SN_V2_FILE_LIBRARY_URL: string;
  AWB_BASE_URL: string;
}

export enum EnvType {
  JUPYTERLAB = 'jupyterlab',
  JUPYTERLITE = 'jupyterlite',
  LOCAL = 'local'
}

export enum Mode {
  LEARN = 'learn',
  AUTHOR = 'author'
}

/**
 * Get the server base URL
 *
 * @param settings the server connection settings
 * @returns the server base URL
 */

const getServerBaseUrl = (settings: ServerConnection.ISettings): string => {
  let baseUrl = settings.baseUrl;
  // Add the trailing slash if it is missing.
  if (!baseUrl.endsWith('/')) {
    baseUrl += '/';
  }
  return baseUrl;
};

/**
 * Extracts the environment type. Will first try to get the type via the URL. The backup is to
 * guess the type from the URL path or host. If nothing was found then default to {@link EnvType.LOCAL}.
 *
 * @returns the environment type
 */
export const ENV_TYPE: EnvType = (function () {
  const currentURL = window.location.href;
  const url = new URL(currentURL);
  const params = url.searchParams;
  let env_type = params.get('env_type');

  if (
    env_type !== EnvType.JUPYTERLAB &&
    env_type !== EnvType.JUPYTERLITE &&
    env_type !== EnvType.LOCAL
  ) {
    console.log('Valid env_type not found in URL parameters');

    if (url.pathname.includes(EnvType.JUPYTERLITE)) {
      console.log('Guessed env_type from URL pathname');
      env_type = EnvType.JUPYTERLITE;
    } else if (url.host.includes(EnvType.JUPYTERLAB)) {
      console.log('Guessed env_type from URL hostname');
      env_type = EnvType.JUPYTERLAB;
    } else {
      console.log('Using default env_type');
      env_type = EnvType.LOCAL;
    }
  } else {
    console.log('env_type found in URL parameters');
  }

  console.log('Environment Type (env_type):', env_type);

  return env_type as EnvType;
})();

/**
 * Extracts the session mode. Will first try to get the {@link Mode} via the URL. If nothing was found
 * then default to {@link Mode.LEARN} unless the environment type is {@link EnvType.LOCAL}.
 *
 * @returns the mode
 */
export const MODE: Mode = (function () {
  const currentURL = window.location.href;
  const params = new URL(currentURL).searchParams;
  let mode_param = params.get('mode');

  if (mode_param !== Mode.AUTHOR && mode_param !== Mode.LEARN) {
    console.log('Valid mode not found in URL parameters');

    if (ENV_TYPE === EnvType.LOCAL) {
      console.log('Using author mode for local environment');
      mode_param = Mode.AUTHOR;
    } else {
      console.log('Using default mode');
      mode_param = Mode.LEARN;
    }
  }

  console.log('Mode:', mode_param);

  return mode_param as Mode;
})();

/**
 * Fetch the configuration from the server
 *
 * @returns the configuration
 */
const CONFIG = async (): Promise<IConfiguration> => {
  const init: RequestInit = {
    method: 'GET'
  };
  const settings = ServerConnection.makeSettings();
  const requestUrl =
    getServerBaseUrl(settings) + 'skillsnetwork_jupyter_extension/config';
  const response = await ServerConnection.makeRequest(
    requestUrl,
    init,
    settings
  );
  return (await response.json()) as IConfiguration;
};

/**
 * Extracts a parameter from the URL. If the parameter is not found in the URL then fetch the parameter from the server.
 * Skip the server request if the environment type is {@link EnvType.JUPYTERLITE} or if the mode is {@link Mode.LEARN}.
 *
 * @param param the parameter to extract from the URL
 * @param configKey the key to use to fetch the parameter from the server
 * @returns the parameter value
 */
const param = async (
  param: string,
  configKey: keyof IConfiguration
): Promise<string> => {
  const currentUrl = window.location.href;

  const parameters = new URL(currentUrl).searchParams;
  const baseUrl: string | undefined = parameters.get(param)!;

  console.log(`${configKey} from current url: ${baseUrl}`);

  if (baseUrl === null) {
    if (ENV_TYPE === EnvType.JUPYTERLITE) {
      console.log(
        `${param} not found in URL parameters, leaving empty due to env_type...`
      );
      return '';
    } else if (MODE === Mode.LEARN) {
      console.log(
        `${param} not found in URL parameters, leaving empty due to mode...`
      );
      return '';
    }

    console.log(
      `${param} not found in URL parameters, making server request...`
    );

    const config = await CONFIG();
    console.log(`${configKey} from server: ${config[configKey]}`);
    return config[configKey];
  } else {
    return decodeURIComponent(baseUrl);
  }
};

export const ATLAS_BASE_URL = await param('atlas_base_url', 'ATLAS_BASE_URL');
export const AWB_BASE_URL = await param('awb_base_url', 'AWB_BASE_URL');
export const SN_V2_FILE_LIBRARY_URL = await param(
  'sn_file_library_url',
  'SN_V2_FILE_LIBRARY_URL'
);
export const SN_FILE_LIBRARY_URL = await param(
  'sn_file_library_url',
  'SN_FILE_LIBRARY_URL'
);

/**
 * Extracts a parameter from the URL. If the parameter is not found in the URL then use the fallback value.
 *
 * @param param the parameter to extract from the URL
 * @param fallback the value to use if the parameter is not found in the URL
 * @returns the parameter value if found or the fallback value
 */
const urlParam = (
  param: string,
  decode: boolean,
  fallback: any
): string | null => {
  const currentUrl = window.location.href;
  const parameters = new URL(currentUrl).searchParams;
  const result = parameters.get(param);

  if (result !== null) {
    return decode ? decodeURIComponent(result) : result;
  } else {
    return fallback;
  }
};

export const ATLAS_TOKEN = urlParam('atlas_token', false, 'NO_TOKEN');
export const AWB_TOKEN = urlParam('awb_token', false, 'NO_TOKEN');
export const NOTEBOOK_URL = urlParam('notebook_url', true, null);
export const FILE_PATH = urlParam('file_path', true, null);

/**
 * Sets the default lab name and kernel based on the environment type.
 *
 * @returns the environment type
 */

export const SET_DEFAULT_LAB_NAME_AND_KERNEL = async (): Promise<EnvType> => {
  const env_type = ENV_TYPE;

  if (env_type === EnvType.JUPYTERLAB || env_type === EnvType.LOCAL) {
    // In production, jupyterlab doesn't have python3 as a kernel option so use python
    Globals.PY_KERNEL_NAME = await GET_PYKERNEL();
    Globals.DEFAULT_LAB_NAME = 'lab.ipynb';
  } else if (env_type === EnvType.JUPYTERLITE) {
    Globals.PY_KERNEL_NAME = 'python';
    Globals.DEFAULT_LAB_NAME = 'lab.jupyterlite.ipynb';
  }

  return env_type;
};

/**
 * Gets the python kernel. If more than one python kernel is found, prioritize python3. If only one python kernel is found, select that kernel
 *
 * @returns the python kernel name
 */
export const GET_PYKERNEL = async (): Promise<string> => {
  // Get the available kernels
  const kspecs = await (await KernelSpecAPI.getSpecs()).kernelspecs;

  function checkPython(spec: string) {
    return spec.includes('python');
  }

  const keys = Object.keys(kspecs);
  // filter for only the spec names with python in it, sorted
  const filtered_keys = keys.filter(checkPython).sort();
  // return the priority python
  const pykernel = filtered_keys[filtered_keys.length - 1];

  return pykernel;
};

// Global variables
export class Globals {
  public static TOKENS: Map<string, string> = new Map<string, string>();
  public static PY_KERNEL_NAME: string;
  public static DEFAULT_LAB_NAME: string;
  public static SHOW_PUBLISH_BUTTON_FOR: string | undefined = undefined;
  public static readonly PREV_PUB_HASH: string = 'prev_pub_hash' as const;
  public static readonly BACKUP_EXT: string = '.backup' as const;
}
