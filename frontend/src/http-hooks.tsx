import { useCallback, useRef, useState, useEffect } from 'react';

// export const useHttpClient = ():void => {
//     const activeHttpRequests = useRef([]);

//     const sendHttpRequest = useCallback(
//         async (url, method = "GET", body = null, headers= {}) => {
//             const httpAbortController = new AbortController();
//             activeHttpRequests.current.push(httpAbortController);
//         },
//     []);
// }