version = $(shell cat .version)
#url = https://devapi.edlumin.com/swagger/v$(word 1,$(subst ., ,$(version)))/swagger.json
url = https://api.redroverk12.com/swagger/v$(word 1,$(subst ., ,$(version)))/swagger.json
local_schema = schema_v$(word 1,$(subst ., ,$(version))).json
generatedDirs = docs redrover_api test dist
versionDot = $(word 1,$(subst ., ,$version))
# containerVersion = v4.3.1  # original
# containerVersion = v5.4.0  # latest 5 release  
# containerVersion = v6.1.0  # lastest python client from 5 release
# containerVersion = v6.6.0  # lastest 6 release with python-experimental
containerVersion = v7.2.0  # lastest 7 release with python-nextgen


# We have to download the schema and adjust all the Enums to be a string.
.PHONY:  download
download: check
	docker run --rm docker.io/jorgeandrada/alpine-jq:latest \
		wget -q -O- ${url} | \
		jq '.components.schemas.AbsenceReasonTrackingTypeEnum.type = "string" | del(.components.schemas.AbsenceReasonTrackingTypeEnum.format)' | \
		jq '.components.schemas.ApprovalStatusEnum.type = "string" | del(.components.schemas.ApprovalStatusEnum.format)' | \
		jq '.components.schemas.CountryEnum.type = "string" | del(.components.schemas.CountryEnum.format)' | \
		jq '.components.schemas.DayOfWeek.type = "string" | del(.components.schemas.DayOfWeek.format)' | \
		jq '.components.schemas.DayPartEnum.type = "string" | del(.components.schemas.DayPartEnum.format)' | \
		jq '.components.schemas.FileFormat.type = "string" | del(.components.schemas.FileFormat.format)' | \
		jq '.components.schemas.FillStatusEnum.type = "string" | del(.components.schemas.FillStatusEnum.format)' | \
		jq '.components.schemas.NeedsReplacementEnum.type = "string" | del(.components.schemas.NeedsReplacementEnum.format)' | \
		jq '.components.schemas.PositionScheduleModeEnum.type = "string" | del(.components.schemas.PositionScheduleModeEnum.format)' | \
		jq '.components.schemas.StateEnum.type = "string" | del(.components.schemas.StateEnum.format)' | \
		jq '.components.schemas.UserRoles.type = "string" | del(.components.schemas.UserRoles.format)' > $(local_schema)

generate: check clean download
	docker run -it --rm -v ${PWD}:/local docker.io/openapitools/openapi-generator-cli:${containerVersion} \
		java -Xmx8G -jar /opt/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar \
		generate \
			--input-spec /local/$(local_schema) \
			--skip-validate-spec \
			--generator-name python \
			--output /local \
			--package-name redrover_api \
			--additional-properties packageVersion=$(version) \
			--additional-properties projectName=redrover-api \
			--additional-properties infoName="EDUStaff, LLC" \
			--additional-properties infoEmail="contact@edustaff.org" \
			--additional-properties appDescription="contact@edustaff.org" \
			--additional-properties packageUrl=https://github.com/edustaff/redrover-api \
			--git-repo-id redrover-api \
			--git-user-id edustaff > build.log
	@echo "$(version)" > .version
	@echo 
	@echo ------------------------------
	@echo You still have to load to pypi
	@echo vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
	@echo 
	@echo make upload
	@echo


.PHONY: clean
clean:
	@-rm -R $(generatedDirs)

.PHONY: check
check:
ifeq "" "$(version)"
#define version = $(shell cat .version)
	@echo "v$$(version)"
	@echo Warning: version isn\'t defined\;
	@exit 1
else:
	@echo Version $(version)
endif
ifndef url
	@echo Warning: url isn\'t defined\;
	@exit 1
endif
ifeq (,$(findstring v$(word 1,$(subst ., ,$(version))),$(url)))
	@echo Warning: Version mismatch\;
	@echo "Python version: $(version) can not be used with url:"
	@echo "  $(url)"
	@exit 1
endif
	@wget -q -O- https://pypi.org/project/redrover-api/$(version)/ > /dev/null; \
	if [ "$$?" -eq "0" ]; then \
		echo "Python version: $(version) already exists in pypi;"; \
		exit 1; \
	fi


.PHONY: check-pypi
check-pypi:
ifeq (,$(shell python3 -m pip freeze | grep twine))
	@echo Warning: twine is not installed\;
	@exit 1
endif

.PHONY: help
help: check
	@echo $(word 1,$(subst ., ,$(version)))
	@echo $(url)
#	docker run --rm -u $(shell id -u):$(shell id -g) -v ${PWD}:/local openapitools/openapi-generator-cli help generate

.PHONY: upload
upload: check check-pypi
	python3 setup.py sdist bdist_wheel
	twine upload dist/*$(version)*
	@echo 
	@echo -----------------------------
	@echo Please rememeber to add a tag
	@echo vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
	@echo 
	@echo git add .
	@echo git commit -m \"generated version $(version)\"
	@echo git tag -a  v$(version) -m \"new version $(version)\"
	@echo git push --tags

