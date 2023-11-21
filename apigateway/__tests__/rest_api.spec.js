const frisby = require('frisby');
const Joi = require('joi');

const apiId = 'API_ID';
const region = 'REGION';
const host = `https://${apiId}.execute-api.${region}.amazonaws.com`;
const stage = 'Prod';

const timeout = 10 * 1000;

beforeAll(() => {
  frisby.globalSetup({
    request: {
      timeout: timeout,
    },
  });
  frisby.baseUrl(host);
});

describe('REST API', () => {
  it('GET /users', () => {
    const url = new URL(stage + '/users', host);
    return frisby.get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', '*', {
        userId: Joi.string().guid().required(),
      });
  }, timeout);
  it('POST /users', () => {
    const name = 'Mr. REST';
    const url = new URL(stage + '/users', host);
    return frisby.post(url, {
      body: {
        name: name,
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 201)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', {
        userId: Joi.string().guid().required(),
        name: Joi.string(),
      })
      .expect('json', {
        name: name,
      });
  }, timeout);

  it('GET /users/{userId}', () => {
    const userId = '00000000-eeee-0000-0000-000000000000';
    const url = new URL(stage + '/users/' + userId, host);
    return frisby.get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', {
        userId: Joi.string().guid().required(),
      })
      .expect('json', {
        userId: userId,
      });
  }, timeout);
  it('PUT /users/{userId}', () => {
    const userId = '00000000-ffff-0000-0000-000000000000';
    const name = 'Miss REST';
    const url = new URL(stage + '/users/' + userId, host);
    return frisby.put(url, {
      body: {
        name: name,
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', {
        userId: Joi.string().guid().required(),
        name: Joi.string(),
      })
      .expect('json', {
        userId: userId,
        name: name,
      });
  }, timeout);
});

describe('REST API(Sequential)', () => {
  it('GET', () => {
    const url = new URL(stage + '/users', host);
    return frisby.get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypesStrict', Joi.array().items(
        Joi.object({
          userId: Joi.string().guid().required(),
        })
      ).max(10).required())
      .then(res => {
        return Promise.all(res.json.map(item => {
          const userId = item.userId;
          const url = new URL(stage + '/users/' + userId, host);
          return frisby.get(url, {
            headers: {
              'Accept-Language': 'ja',
            }
          })
            //.inspectRequestHeaders()
            //.inspectRequest()
            //.inspectStatus()
            //.inspectHeaders()
            //.inspectBody()
            .expect('status', 200)
            .expect('header', 'Content-Type', 'application/json')
            .expect('jsonTypesStrict', {
              userId: Joi.string().guid().required(),
              languages: Joi.array().items(Joi.string()).min(1).required(),
              token: Joi.string(),
            })
            .expect('json', {
              userId: userId,
            });
        }));
      });
  }, timeout);
});
