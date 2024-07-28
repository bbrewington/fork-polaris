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

import com.fasterxml.jackson.annotation.JsonTypeName;
import io.polaris.core.context.RealmContext;
import io.polaris.service.config.HasEntityManagerFactory;
import io.polaris.service.config.RealmEntityManagerFactory;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.function.Supplier;

@JsonTypeName("symmetric-key")
public class JWTSymmetricKeyFactory implements TokenBrokerFactory, HasEntityManagerFactory {
  private RealmEntityManagerFactory realmEntityManagerFactory;
  private int maxTokenGenerationInSeconds = 3600;
  private String file;
  private String secret;

  @Override
  public TokenBroker apply(RealmContext realmContext) {
    if (file == null && secret == null) {
      throw new IllegalStateException("Either file or secret must be set");
    }
    Supplier<String> secretSupplier = secret != null ? () -> secret : readSecretFromDisk();
    return new JWTSymmetricKeyBroker(
        realmEntityManagerFactory.getOrCreateEntityManager(realmContext),
        maxTokenGenerationInSeconds,
        secretSupplier);
  }

  private Supplier<String> readSecretFromDisk() {
    return () -> {
      try {
        return Files.readString(Paths.get(file));
      } catch (IOException e) {
        throw new RuntimeException("Failed to read secret from file: " + file, e);
      }
    };
  }

  public void setMaxTokenGenerationInSeconds(int maxTokenGenerationInSeconds) {
    this.maxTokenGenerationInSeconds = maxTokenGenerationInSeconds;
  }

  public void setFile(String file) {
    this.file = file;
  }

  public void setSecret(String secret) {
    this.secret = secret;
  }

  @Override
  public void setEntityManagerFactory(RealmEntityManagerFactory entityManagerFactory) {
    this.realmEntityManagerFactory = entityManagerFactory;
  }
}
