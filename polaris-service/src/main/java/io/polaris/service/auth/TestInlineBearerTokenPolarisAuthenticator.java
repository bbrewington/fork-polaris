/*
 * Copyright (c) 2024 Snowflake Computing Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.polaris.service.auth;

import com.google.common.base.Splitter;
import io.dropwizard.auth.AuthenticationException;
import io.polaris.core.PolarisCallContext;
import io.polaris.core.auth.AuthenticatedPolarisPrincipal;
import io.polaris.core.context.CallContext;
import io.polaris.core.entity.PolarisPrincipalSecrets;
import io.polaris.core.persistence.PolarisMetaStoreManager;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * {@link io.dropwizard.auth.Authenticator} that parses a token as a sequence of key/value pairs.
 * Specifically, we expect to find
 *
 * <ul>
 *   <li>principal - the clientId of the principal
 *   <li>realm - the current realm
 * </ul>
 *
 * This class does not expect a client to be either present or correct. Lookup is delegated to the
 * {@link PolarisMetaStoreManager} for the current realm.
 */
public class TestInlineBearerTokenPolarisAuthenticator extends BasePolarisAuthenticator {
  private static final Logger LOGGER =
      LoggerFactory.getLogger(TestInlineBearerTokenPolarisAuthenticator.class);

  @Override
  public Optional<AuthenticatedPolarisPrincipal> authenticate(String credentials)
      throws AuthenticationException {
    Map<String, String> properties = extractPrincipal(credentials);
    PolarisMetaStoreManager metaStoreManager =
        entityManagerFactory
            .getOrCreateEntityManager(CallContext.getCurrentContext().getRealmContext())
            .getMetaStoreManager();
    PolarisCallContext callContext = CallContext.getCurrentContext().getPolarisCallContext();
    String principal = properties.get("principal");

    LOGGER.info("Checking for existence of principal {} in map {}", principal, properties);

    TokenInfoExchangeResponse tokenInfo = new TokenInfoExchangeResponse();
    tokenInfo.setSub(principal);
    tokenInfo.setScope(properties.get("role"));

    PolarisPrincipalSecrets secrets =
        metaStoreManager.loadPrincipalSecrets(callContext, principal).getPrincipalSecrets();
    if (secrets == null) {
      // For test scenarios, if we're allowing short-circuiting into the bearer flow, there may
      // not be a clientId/clientSecret, and instead we'll let the BasePolarisAuthenticator
      // resolve the principal by name from the persistence store.
      LOGGER.warn("Failed to load secrets for principal {}", principal);
    } else {
      tokenInfo.setIntegrationId(secrets.getPrincipalId());
    }

    return getPrincipal(tokenInfo);
  }

  private static Map<String, String> extractPrincipal(String credentials) {
    if (credentials.contains(";") || credentials.contains(":")) {
      Map<String, String> parsedProperties = new HashMap<>();
      parsedProperties.putAll(
          Splitter.on(';').trimResults().withKeyValueSeparator(':').split(credentials));
      return parsedProperties;
    }
    return Map.of();
  }
}
