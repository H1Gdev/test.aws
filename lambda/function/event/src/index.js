const { Logger } = require('@aws-lambda-powertools/logger');
const { getParameter } = require('@aws-lambda-powertools/parameters/ssm');
const { STS, GetCallerIdentityCommand } = require('@aws-sdk/client-sts');
const _ = require('lodash');

const logger = new Logger();

exports.handler = async (event/* Request */, context) => {
  logger.addContext(context);

  // User
  if (event.queryStringParameters?.user) {
    const sts = new STS({});
    const getCallerIdentityCommand = new GetCallerIdentityCommand({});
    const stsResponse = await sts.send(getCallerIdentityCommand);
    // AWS_PROFILE > 'default'
    logger.info(`[User]${stsResponse.Arn}`);
  }

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

  // Parameters
  if (event.queryStringParameters?.ssm) {
    const value = await getParameter('/my/parameter');
    logger.info(`[Parameters]${value}`);
  }

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
