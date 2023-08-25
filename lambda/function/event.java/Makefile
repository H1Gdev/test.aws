# https://github.com/aws/aws-lambda-builders/issues/138

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/building-custom-runtimes.html
build-EventJavaFunction:
	gradle build
ifdef ARTIFACTS_DIR
	unzip -d $(ARTIFACTS_DIR) $(CURDIR)/build/libs/*.jar
endif
