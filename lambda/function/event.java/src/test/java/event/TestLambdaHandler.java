package event;

import com.amazonaws.services.lambda.runtime.ClientContext;
import com.amazonaws.services.lambda.runtime.CognitoIdentity;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import java.util.Map;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

// https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html
import static org.junit.jupiter.api.Assertions.assertEquals;

class TestLambdaHandler {
    @BeforeAll
    static void setupAll() {
    }

    @Test
    void test() {
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(200, response.getStatusCode());
    }

    @Test
    void testUser() {
        Map<String, String> queryStringParameters = Map.of("user", Boolean.toString(true));
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(200, response.getStatusCode());
    }

    @ParameterizedTest
    @ValueSource(strings = {"fatal", "error", "warn", "info", "debug", "trace", ""})
    void testLogging(String level) {
        Map<String, String> queryStringParameters = Map.of("log", level);
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(200, response.getStatusCode());
    }

    @Test
    void testParameters() {
        Map<String, String> queryStringParameters = Map.of("ssm", Boolean.toString(true));
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(200, response.getStatusCode());
    }

    // https://docs.aws.amazon.com/lambda/latest/dg/java-context.html
    static class LambdaContext implements Context {
        public String getAwsRequestId() {
            return "test-test";
        }
        public String getLogGroupName() {
            return "/aws/lambda/event";
        }
        public String getLogStreamName() {
            return "test";
        }
        public String getFunctionName() {
            return "event";
        }
        public String getFunctionVersion() {
            return "$LATEST";
        }
        public String getInvokedFunctionArn() {
            return "arn:aws:lambda:REGION:ACCOUNT-ID:function:event";
        }
        public CognitoIdentity getIdentity() {
            return null;
        }
        public ClientContext getClientContext() {
            return null;
        }
        public int getRemainingTimeInMillis() {
            return 300000;
        }
        public int getMemoryLimitInMB() {
            return 512;
        }
        public LambdaLogger getLogger() {
            return new LambdaLogger() {
                public void log(String message) {
                }
                public void log(byte[] message) {
                }
            };
        }
    }
}
