// send a post, update or delete request to the API

async function postUpdateDelete(url, info, reqMethod="POST") {
    // it defaults to a post request if not request method is specified
    let data = null;
    let error = "Request has no errors";
    let statusCode;

    try {
      const res = await fetch(url, {
        method: reqMethod,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(info)
      });
      statusCode = res;
      if (!res.ok) { // error coming back from server
        const error_data = await res.json();
        throw Error(error_data.message);
      };
      const resp_data = await res.json();
      data = resp_data;
    } catch(err) {
      // auto catches network / connection error
      error = err.message;
    };
    return {data, error, statusCode};
}

export default postUpdateDelete;
