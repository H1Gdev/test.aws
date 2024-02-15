using System.Net;
using Xunit;
using Amazon.Lambda.APIGatewayEvents;
using Amazon.Lambda.TestUtilities;

namespace Event.Tests;

// [xUnit.net](https://xunit.net/)

public class LambdaHandlerTest
{
    [Fact]
    public async void Test()
    {
        var request = new APIGatewayProxyRequest();
        var context = new TestLambdaContext();
        var lambdaHandler = new LambdaHandler();
        var response = await lambdaHandler.HandleRequest(request, context);
        Assert.Equal((int)HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async void TestUser()
    {
        var request = new APIGatewayProxyRequest
        {
            QueryStringParameters = new Dictionary<string, string>
            {
                { "user", "true" }
            },
        };
        var context = new TestLambdaContext();
        var lambdaHandler = new LambdaHandler();
        var response = await lambdaHandler.HandleRequest(request, context);
        Assert.Equal((int)HttpStatusCode.OK, response.StatusCode);
    }

    [Theory]
    [InlineData("critical")]
    [InlineData("error")]
    [InlineData("warn")]
    [InlineData("info")]
    [InlineData("debug")]
    [InlineData("trace")]
    public async void TestLogging(string level)
    {
        var request = new APIGatewayProxyRequest
        {
            QueryStringParameters = new Dictionary<string, string>
            {
                { "log", level }
            },
        };
        var context = new TestLambdaContext();
        var lambdaHandler = new LambdaHandler();
        var response = await lambdaHandler.HandleRequest(request, context);
        Assert.Equal((int)HttpStatusCode.OK, response.StatusCode);
    }

    [Theory]
    [InlineData("correlation_id_value")]
    [InlineData("")]
    [InlineData(null)]
    public async void TestCorrelationId(string correlationId)
    {
        var request = new APIGatewayProxyRequest
        {
            QueryStringParameters = new Dictionary<string, string>
            {
                { "log", "info" }
            },
            RequestContext = new APIGatewayProxyRequest.ProxyRequestContext
            {
                RequestId = correlationId,
            },
        };
        var context = new TestLambdaContext();
        var lambdaHandler = new LambdaHandler();
        var response = await lambdaHandler.HandleRequest(request, context);
        Assert.Equal((int)HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async void TestParameters()
    {
        var request = new APIGatewayProxyRequest
        {
            QueryStringParameters = new Dictionary<string, string>
            {
                { "ssm", "true" }
            },
        };
        var context = new TestLambdaContext();
        var lambdaHandler = new LambdaHandler();
        var response = await lambdaHandler.HandleRequest(request, context);
        Assert.Equal((int)HttpStatusCode.OK, response.StatusCode);
    }
}
