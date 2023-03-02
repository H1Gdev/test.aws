const frisby = require('frisby');
const Joi = require('joi');

// https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-from-example.html
const host = 'http://petstore-demo-endpoint.execute-api.com';
const stage = 'petstore';

beforeAll(() => {
  frisby.baseUrl(host);
});

const types = ['dog', 'cat', 'fish', 'bird', 'gecho'];

describe('Amazon API Gateway Example', () => {
  it.skip('GET /', () => {
    return frisby.get(stage + '/')
      .expect('status', 200)
      .expect('header', 'Content-Type', 'text/html');
  });
  it('GET /pets', () => {
    return frisby.get(stage + '/pets')
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', Joi.array())
      .expect('jsonTypesStrict', '*', {
        'id': Joi.number().integer().required(),
        'type': Joi.string().allow(...types).required(),
        'price': Joi.number().required(),
      });
  });
  it('POST /pets', () => {
    return frisby.post(stage + '/pets', {
      body: {
        'type': 'bird',
        'price': 66.30
      }
    })
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypesStrict', {
        'pet': {
          'type': Joi.string().allow(...types).required(),
          'price': Joi.number().required(),
        },
        'message': Joi.string().required(),
      });
  });
  it('POST /pets (Error)', () => {
    return frisby.post(stage + '/pets', {
      body: {
      }
    })
      .expect('status', 400)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypes', 'errors', Joi.array());
  });
  it('GET /pets/{petId}', () => {
    const petId = '1';
    return frisby.get(stage + '/pets/' + petId)
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('jsonTypesStrict', {
        'id': Joi.number().integer().required(),
        'type': Joi.string().allow(...types).required(),
        'price': Joi.number().required(),
      });
  });

  it.skip('OPTIONS /pets', () => {
    return frisby.options(stage + '/pets')
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('header', 'access-control-allow-origin')
      .expect('header', 'access-control-allow-methods', /GET/)
      .expect('header', 'access-control-allow-methods', /POST/)
      .expect('header', 'access-control-allow-methods', /OPTIONS/)
      .expect('header', 'access-control-allow-headers', /Content-Type/);
  });
  it.skip('OPTIONS /pets/{petId}', () => {
    const petId = '1';
    return frisby.options(stage + '/pets/' + petId)
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json')
      .expect('header', 'access-control-allow-origin')
      .expect('header', 'access-control-allow-methods', /GET/)
      .expect('header', 'access-control-allow-methods', /OPTIONS/)
      .expect('header', 'access-control-allow-headers', /Content-Type/);
  });
});
