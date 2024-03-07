using System.Net;
using System.Text.Json;
using System.Threading;
// https://github.com/aws/aws-lambda-dotnet/
using Amazon.Lambda.APIGatewayEvents;
using Amazon.Lambda.Core;
// https://github.com/aws/aws-sdk-net/
using Amazon.SecurityToken;
using Amazon.SecurityToken.Model;
// https://github.com/aws-powertools/powertools-lambda-dotnet
using AWS.Lambda.Powertools.Logging;
using AWS.Lambda.Powertools.Parameters;
using AWS.Lambda.Powertools.Parameters.SimpleSystemsManagement;
using AWS.Lambda.Powertools.Tracing;

// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace Event;

// https://docs.aws.amazon.com/lambda/latest/dg/csharp-handler.html
public class LambdaHandler
{
    private readonly ISsmProvider _ssmProvider = ParametersManager.SsmProvider;

    public LambdaHandler()
    {
#if false
        Tracing.RegisterForAllServices();
#else
        Tracing.Register<IAmazonSecurityTokenService>();
#endif
    }

    [Logging(CorrelationIdPath = CorrelationIdPaths.ApiGatewayRest, ClearState = true)]
    // Tracing requires ASP.NET Core Runtime.
    [Tracing]
    public async Task<APIGatewayProxyResponse> HandleRequest(APIGatewayProxyRequest request, ILambdaContext context)
    {
        // User
        if (request.QueryStringParameters?.ContainsKey("user") ?? default)
        {
            var client = new AmazonSecurityTokenServiceClient();
            var callerIdRequest = new GetCallerIdentityRequest();
            var caller = await client.GetCallerIdentityAsync(callerIdRequest);
            // AWS_PROFILE > 'default'
            Logger.LogInformation($"[User]{caller.Arn}");
        }

        // Logging
        switch(request.QueryStringParameters?.ContainsKey("log") ?? default ? request.QueryStringParameters?["log"] : string.Empty)
        {
            case "critical":
                Logger.LogCritical($"[CRITICAL]{JsonSerializer.Serialize(request)}");
                goto case "error";
            case "error":
                Logger.LogError($"[ERROR]{JsonSerializer.Serialize(request)}");
                goto case "warn";
            case "warn":
                Logger.LogWarning($"[WARN]{JsonSerializer.Serialize(request)}");
                goto case "info";
            case "info":
                Logger.LogInformation($"[INFO]{JsonSerializer.Serialize(request)}");
                goto case "debug";
            case "debug":
                Logger.LogDebug($"[DEBUG]{JsonSerializer.Serialize(request)}");
                goto case "trace";
            case "trace":
                Logger.LogTrace($"[TRACE]{JsonSerializer.Serialize(request)}");
                break;
            default:
                Console.WriteLine($"[Console.WriteLine]({Environment.ProcessId},{Thread.CurrentThread.ManagedThreadId}){JsonSerializer.Serialize(request)}");
                break;
        }

        // Parameters
        if (request.QueryStringParameters?.ContainsKey("ssm") ?? default)
        {
            var value = await _ssmProvider
                .GetAsync("/my/parameter")
                .ConfigureAwait(false);
            Logger.LogInformation($"[Parameters]{value}");
        }

        // Response
        var response = new APIGatewayProxyResponse
        {
            StatusCode = (int)HttpStatusCode.OK,
            Headers = new Dictionary<string, string>
            {
                { "Content-Type", "application/json" }
            },
        };
        return response;
    }
}
