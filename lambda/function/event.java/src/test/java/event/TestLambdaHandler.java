package event;

import com.amazonaws.services.lambda.runtime.ClientContext;
import com.amazonaws.services.lambda.runtime.CognitoIdentity;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import java.net.HttpURLConnection;
import java.util.Map;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EmptySource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
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
        assertEquals(HttpURLConnection.HTTP_OK, response.getStatusCode());
    }

    @Test
    void testUser() {
        Map<String, String> queryStringParameters = Map.of("user", Boolean.toString(true));
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(HttpURLConnection.HTTP_OK, response.getStatusCode());
    }

    @ParameterizedTest
    @ValueSource(strings = {"fatal", "error", "warn", "info", "debug", "trace"})
    @EmptySource
    void testLogging(String level) {
        Map<String, String> queryStringParameters = Map.of("log", level);
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(HttpURLConnection.HTTP_OK, response.getStatusCode());
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"correlation_id_value"})
    void testCorrelationId(String correlationId) {
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent()
            .withQueryStringParameters(Map.of("log", "info"))
            .withRequestContext(new APIGatewayProxyRequestEvent.ProxyRequestContext()
                .withRequestId(correlationId));
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(HttpURLConnection.HTTP_OK, response.getStatusCode());
    }

    @Test
    void testParameters() {
        Map<String, String> queryStringParameters = Map.of("ssm", Boolean.toString(true));
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        event.setQueryStringParameters(queryStringParameters);
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, new LambdaContext());
        assertEquals(HttpURLConnection.HTTP_OK, response.getStatusCode());
    }

    // https://docs.aws.amazon.com/lambda/latest/dg/java-context.html
    static class LambdaContext implements Context {
        private static final int REMAINING_TIME_IN_MILLIS = 300000;
        private static final int MEMORY_LIMIT_IN_MB = 512;
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
            return REMAINING_TIME_IN_MILLIS;
        }
        public int getMemoryLimitInMB() {
            return MEMORY_LIMIT_IN_MB;
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
