import { buildQueryURL } from './linkBuilder';
import ApiError from './apiError';
const timeoutDuration = 60000;

const serverURL = process.env.REACT_APP_SERVER_URL;

export default function apiCall(route, params, body, method, token, contentType) {
  const request = new Promise((resolve, reject) => {
    // Code for fetch will be written here
    const headers = new Headers({
      'Content-Type': contentType ? contentType : 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Accept': 'application/json'
    });
    const requestDetails = {
      method,
      mode: 'cors',
      headers,
    };
    if (method !== 'GET') requestDetails.body = JSON.stringify(body);

    const url = buildQueryURL(`${serverURL}/${route}`, params);

    console.log(url);
    if (!process.env.NODE_ENV === 'production') {
      console.log(`api call to ${url}`);
    }

    fetch(url, requestDetails)
      .then(handleErrors)
      .then((response) => response.text())
      .then((text) => resolve(text.length ? JSON.parse(text) : {}))
      .catch(reject);
  });

  const timeout = new Promise((resolve, reject) => {
    setTimeout(reject, timeoutDuration, 'Request timed out!');
  });

  return new Promise((resolve, reject) => {
    Promise.race([request, timeout])
      .then(resolve)
      .catch(reject);
  });
}

async function handleErrors(response) {
  if (response.ok) {
    return response;  
  } else if (response.status === 400) {
    const text = await response.text();
    const errorObject = JSON.parse(text);
    //TODO remove response.url on production
    let message = errorObject.title
      || errorObject.Title
      || errorObject.message
      || errorObject.Message
      || 'Bad Request';

    const formErrors = errorObject.errors ? errorObject.errors : {};
    throw new ApiError(formErrors, response.status, message);
  } else if (response.status === 404) {
    throw new ApiError({}, response.status, 'Not Found');
  } else if (response.status === 409) {
    const text = await response.text();
    const errorObject = JSON.parse(text);
    throw new ApiError({}, response.status, errorObject);
  }
  throw new ApiError({}, response.status, 'Server Error');
}