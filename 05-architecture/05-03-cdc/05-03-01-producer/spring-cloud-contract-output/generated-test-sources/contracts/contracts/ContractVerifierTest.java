package contracts;

import contracts.RestBase;
import com.jayway.jsonpath.DocumentContext;
import com.jayway.jsonpath.JsonPath;
import org.junit.Test;
import org.junit.Rule;
import org.junit.FixMethodOrder;
import org.junit.runners.MethodSorters;
import io.restassured.specification.RequestSpecification;
import io.restassured.response.Response;

import static org.springframework.cloud.contract.verifier.assertion.SpringCloudContractAssertions.assertThat;
import static org.springframework.cloud.contract.verifier.util.ContractVerifierUtil.*;
import static com.toomuchcoding.jsonassert.JsonAssertion.assertThatJson;
import static io.restassured.RestAssured.*;

@SuppressWarnings("rawtypes")
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class ContractVerifierTest extends RestBase {

	@Test
	public void validate_01_should_return_fraud() throws Exception {
		// given:
			RequestSpecification request = given()
					.header("Content-Type", "application/json")
					.body("{\"uuid\":\"89c878e3-38f7-4831-af6c-c3b4a0669022\",\"person\":{\"name\":\"Stefania\",\"surname\":\"Stefanowska\",\"date_of_birth\":\"2020-01-01\",\"gender\":\"FEMALE\",\"national_id_number\":\"1234567890\"}}");

		// when:
			Response response = given().spec(request)
					.post("/fraudCheck");

		// then:
			assertThat(response.statusCode()).isEqualTo(401);
	}

	@Test
	public void validate_02_should_return_non_fraud() throws Exception {
		// given:
			RequestSpecification request = given()
					.header("Content-Type", "application/json")
					.body("{\"uuid\":\"6cb4521f-49da-48e5-9ea2-4a1d3899581d\",\"person\":{\"name\":\"Jacek\",\"surname\":\"Dubilas\",\"date_of_birth\":\"1980-03-08\",\"gender\":\"MALE\",\"national_id_number\":\"80030818293\"}}");

		// when:
			Response response = given().spec(request)
					.post("/fraudCheck");

		// then:
			assertThat(response.statusCode()).isEqualTo(200);
	}

}
