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
import org.apache.commons.lang3.StringUtils;

public class LambdaHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent event, Context context) {
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
