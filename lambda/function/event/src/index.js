const { Logger } = require('@aws-lambda-powertools/logger');
const _ = require('lodash');

const logger = new Logger();

exports.handler = async (event/* Request */, context) => {
  logger.addContext(context);

  // Logger
  /* eslint-disable no-fallthrough */
  switch (event.queryStringParameters?.log) {
  case 'critical':
    logger.critical('[CRITICAL]', event);
  case 'error':
    logger.error('[ERROR]', event);
  case 'warn':
    logger.warn('[WARN]', event);
  case 'info':
    logger.info('[INFO]', event);
  case 'debug':
    logger.debug('[DEBUG]', event);
    break;
  default:
    console.log('[console.log]', event);
    break;
  }
  /* eslint-enable no-fallthrough */

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
