package event;

import com.amazonaws.services.lambda.runtime.ClientContext;
import com.amazonaws.services.lambda.runtime.CognitoIdentity;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

// https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html
import static org.junit.jupiter.api.Assertions.assertEquals;

class TestLambdaHandler {
    @BeforeAll
    static void setupAll() {
    }

    @Test
    void test() {
        APIGatewayProxyRequestEvent event = new APIGatewayProxyRequestEvent();
        Context context = new TestContext();
        LambdaHandler handler = new LambdaHandler();
        APIGatewayProxyResponseEvent response = handler.handleRequest(event, context);
        assertEquals(200, response.getStatusCode());
    }

    // https://docs.aws.amazon.com/lambda/latest/dg/java-context.html
    static class TestContext implements Context {
        public String getAwsRequestId() {
            return "test.AwsRequestId";
        }
        public String getLogGroupName() {
            return "/aws/lambda/function";
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
            return "test.ARN";
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
