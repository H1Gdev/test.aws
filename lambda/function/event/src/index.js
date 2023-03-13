const _ = require('lodash');

exports.handler = async (event/* Request */, context) => {
  // Response
  const response = {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      event: event,
      context: context,
      lodash: _.VERSION,
    }),
  };
  return response;
};
