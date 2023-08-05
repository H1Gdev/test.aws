package event;

// [AWS Lambda Sample]
// https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps
//
// https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/java-events
// - Java, Gradle, Event handlers
// https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/s3-java
// - Java, Amazon S3

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import java.util.Map;
import java.util.Optional;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;
import software.amazon.awssdk.http.apache.ApacheHttpClient;
import software.amazon.awssdk.services.sts.StsClient;
import software.amazon.awssdk.services.sts.model.GetCallerIdentityRequest;
import software.amazon.awssdk.services.sts.model.GetCallerIdentityResponse;
import software.amazon.lambda.powertools.logging.Logging;
import software.amazon.lambda.powertools.parameters.Param;

public class LambdaHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    private static final Logger LOG = LogManager.getLogger();

    // Parameters
    @Param(key = "/my/parameter")
    private String paramValue;

    @Logging
    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent event, Context context) {
        // User
        if (Optional.ofNullable(event.getQueryStringParameters()).map(p -> p.get("user")).isPresent()) {
            StsClient stsClient = StsClient.builder()
                // "software.amazon.lambda:powertools-parameters" depends on "software.amazon.awssdk:url-connection-client", so SdkClientException occurs if HttpClient is not specified.
                .httpClientBuilder(ApacheHttpClient.builder())
                .build();
            GetCallerIdentityRequest getCallerIdentityRequest = GetCallerIdentityRequest.builder().build();
            GetCallerIdentityResponse getCallerIdentityResponse = stsClient.getCallerIdentity(getCallerIdentityRequest);
            // AWS_PROFILE > 'default'
            LOG.info("[User]" + getCallerIdentityResponse.arn());
        }

        // Logging
        switch (Optional.ofNullable(event.getQueryStringParameters()).map(p -> p.get("log")).orElse(StringUtils.EMPTY)) {
            case "fatal":
                LOG.fatal("[FATAL]" + event);
            case "error":
                LOG.error("[ERROR]" + event);
            case "warn":
                LOG.warn("[WARN]" + event);
            case "info":
                LOG.info("[INFO]" + event);
            case "debug":
                LOG.debug("[DEBUG]" + event);
            case "trace":
                LOG.trace("[TRACE]" + event);
                break;
            default:
                System.out.println("[System.out.println]" + event);
                break;
        }

        // Parameters
        if (Optional.ofNullable(event.getQueryStringParameters()).map(p -> p.get("ssm")).isPresent()) {
            // - Transformer consumes resources, so should not be used for Primitive types.
            LOG.info("[Parameters]" + paramValue);
        }

        // Response
        APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent();
        response.setIsBase64Encoded(false);
        response.setStatusCode(200);
        Map<String, String> headers = Map.of("Content-Type", "application/json");
        response.setHeaders(headers);
        response.setBody(
	        "{" +
	        "  \"event\": {" +
	        "    \"body\": \"" + StringUtils.defaultString(event.getBody()).replace("\"", "") + "\"" +
	        "  }," +
	        "  \"context\": \"" + context + "\"" +
	        "}"
        );
        return response;
    }
}
