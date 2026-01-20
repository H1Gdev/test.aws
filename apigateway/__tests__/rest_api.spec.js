const frisby = require('frisby');
const Joi = require('joi');

const apiId = 'API_ID';
const region = 'REGION';
const apiKey = 'API_KEY'
const host = `https://${apiId}.execute-api.${region}.amazonaws.com`;
const stage = 'Prod';

const timeout = 10 * 1000;

beforeAll(() => {
  frisby.globalSetup({
    request: {
      headers: {
        'X-API-KEY': apiKey,
      },
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
  it('GET /users?version=1', () => {
    const url = new URL(stage + '/users', host);
    url.searchParams.append('version', '1');
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

  it('GET /users/{userId}/icon', () => {
    const userId = '00000000-gggg-0000-0000-000000000000';
    const url = new URL(stage + '/users/' + userId + '/icon', host);
    return frisby.setup({ request: { rawBody: true } })
      .get(url, {
        headers: {
          Accept: 'image/png',
        }
      })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'image/png')
      .then(res => {
        let body = res.body;
        expect(body.byteLength).toBeGreaterThan(8);
        expect(String.fromCharCode.apply(null, new Uint8Array(body.slice(1, 4)))).toEqual('PNG');
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
              apiKey: Joi.string(),
              token: Joi.string(),
            })
            .expect('json', {
              userId: userId,
            });
        }));
      });
  }, timeout);
});

describe('REST API with check CORS', () => {
  const checkCORS = (url, origin, method) => {
    return frisby.options(url, {
      headers: {
        'Origin': origin,
        'Access-Control-Request-Method': method,
        'Access-Control-Request-Headers': 'Content-Type',
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      // [CorsConfiguration]AllowHeaders value
      .expect('header', 'access-control-allow-headers')
      .expect('header', 'access-control-allow-headers', /^\*$|Content-Type/)
      // [CorsConfiguration]AllowMethods value
      .expect('header', 'access-control-allow-methods')
      .expect('header', 'access-control-allow-methods', new RegExp(method))
      // [CorsConfiguration]AllowOrigin value
      .expect('header', 'access-control-allow-origin')
      .expect('header', 'access-control-allow-origin', new RegExp(`^\\*$|${(origin != null ? origin.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&') : '')}`));
  };

  const origin = 'http://www.example.com';
  it('GET /users', () => {
    const url = new URL(stage + '/users', host);
    return checkCORS(url, origin, 'GET')
      .then(res => {
        const accessControlAllowHeaders = res.headers.get('access-control-allow-headers');
        const accessControlAllowOrigin = res.headers.get('access-control-allow-origin');

        return frisby.get(url)
          //.inspectHeaders()
          .expect('status', 200)
          .expect('header', 'Content-Type', 'application/json')
          // value exactly matches that of OPTIONS.
          .expect('header', 'access-control-allow-headers', new RegExp(`^${accessControlAllowHeaders.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('header', 'access-control-allow-origin', new RegExp(`^${accessControlAllowOrigin.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('jsonTypes', '*', {
            userId: Joi.string().guid().required(),
          });
      });
  }, timeout);
  it('POST /users', () => {
    const url = new URL(stage + '/users', host);
    return checkCORS(url, origin, 'POST')
      .then(res => {
        const accessControlAllowHeaders = res.headers.get('access-control-allow-headers');
        const accessControlAllowOrigin = res.headers.get('access-control-allow-origin');

        const name = 'Mr. REST';
        return frisby.post(url, {
          body: {
            name: name,
          }
        })
          //.inspectHeaders()
          .expect('status', 201)
          .expect('header', 'Content-Type', 'application/json')
          .expect('header', 'access-control-allow-headers', new RegExp(`^${accessControlAllowHeaders.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('header', 'access-control-allow-origin', new RegExp(`^${accessControlAllowOrigin.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('jsonTypes', {
            userId: Joi.string().guid().required(),
            name: Joi.string(),
          })
          .expect('json', {
            name: name,
          });
      });
  }, timeout);

  it('GET /users/{userId}', () => {
    const userId = '00000000-eeee-0000-0000-000000000000';
    const url = new URL(stage + '/users/' + userId, host);
    return checkCORS(url, origin, 'GET')
      .then(res => {
        const accessControlAllowHeaders = res.headers.get('access-control-allow-headers');
        const accessControlAllowOrigin = res.headers.get('access-control-allow-origin');

        return frisby.get(url)
          //.inspectHeaders()
          .expect('status', 200)
          .expect('header', 'Content-Type', 'application/json')
          .expect('header', 'access-control-allow-headers', new RegExp(`^${accessControlAllowHeaders.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('header', 'access-control-allow-origin', new RegExp(`^${accessControlAllowOrigin.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('jsonTypes', {
            userId: Joi.string().guid().required(),
          })
          .expect('json', {
            userId: userId,
          });
      });
  }, timeout);
  it('PUT /users/{userId}', () => {
    const userId = '00000000-ffff-0000-0000-000000000000';
    const url = new URL(stage + '/users/' + userId, host);
    return checkCORS(url, origin, 'PUT')
      .then(res => {
        const accessControlAllowHeaders = res.headers.get('access-control-allow-headers');
        const accessControlAllowOrigin = res.headers.get('access-control-allow-origin');

        const name = 'Miss REST';
        return frisby.put(url, {
          body: {
            name: name,
          }
        })
          //.inspectHeaders()
          .expect('status', 200)
          .expect('header', 'Content-Type', 'application/json')
          .expect('header', 'access-control-allow-headers', new RegExp(`^${accessControlAllowHeaders.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('header', 'access-control-allow-origin', new RegExp(`^${accessControlAllowOrigin.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&')}$`))
          .expect('jsonTypes', {
            userId: Joi.string().guid().required(),
            name: Joi.string(),
          })
          .expect('json', {
            userId: userId,
            name: name,
          });
      });
  }, timeout);
});

describe('Error', () => {
  it('No API Key', () => {
    const url = new URL(stage + '/users', host);
    return frisby.setup({
      request: {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        rawBody: false,
        inspectOnFailure: true,
        timeout: timeout,
      },
    }, true).get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 403);
  }, timeout);
  it('Invalid API Key', () => {
    const url = new URL(stage + '/users', host);
    return frisby.get(url, {
      headers: {
        'X-API-KEY': `Invalid_${apiKey}`,
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 403);
  }, timeout);
});
