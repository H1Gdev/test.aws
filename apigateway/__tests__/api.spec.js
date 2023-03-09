const frisby = require('frisby');
const Joi = require('joi');

const apiId = 'API_ID';
const region = 'REGION';
const host = `https://${apiId}.execute-api.${region}.amazonaws.com`;
const stage = 'STAGE'

beforeAll(() => {
  frisby.baseUrl(host);
});

describe('Amazon API Gateway Example', () => {
  it('GET /test', () => {
    const url = new URL(stage + '/test', host);
    url.searchParams.append('q0', 'a');
    return frisby.get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json');
  });
  it('POST /test', () => {
    const url = new URL(stage + '/test', host);
    url.searchParams.append('q0', 'a');
    return frisby.post(url, {
      body: {
        name: 'User',
        type: 'AAA',
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json');
  });

  it('GET /lambda', () => {
    const url = new URL(stage + '/lambda', host);
    url.searchParams.append('q0', 'a');
    return frisby.get(url)
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json');
  });
  it('POST /lambda', () => {
    const url = new URL(stage + '/lambda', host);
    url.searchParams.append('q0', 'a');
    return frisby.post(url, {
      body: {
        name: 'User',
        type: 'AAA',
      }
    })
      //.inspectRequestHeaders()
      //.inspectRequest()
      //.inspectStatus()
      //.inspectHeaders()
      //.inspectBody()
      .expect('status', 200)
      .expect('header', 'Content-Type', 'application/json');
  });
});
