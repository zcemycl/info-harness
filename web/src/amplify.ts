import { Amplify } from "aws-amplify";
import { cognitoUserPoolsTokenProvider } from "aws-amplify/auth/cognito";
import { defaultStorage } from "aws-amplify/utils";

const userPoolId = import.meta.env.VITE_COGNITO_USER_POOL_ID;
const userPoolClientId = import.meta.env.VITE_COGNITO_USER_POOL_CLIENT_ID;
const identityPoolId = import.meta.env.VITE_COGNITO_IDENTITY_POOL_ID;
let configured = false;

export function configureAmplify(): void {
  if (configured) return;
  if (!userPoolId || !userPoolClientId) {
    console.warn("Missing VITE_COGNITO_USER_POOL_ID or VITE_COGNITO_USER_POOL_CLIENT_ID");
    return;
  }

  if (identityPoolId?.trim()) {
    Amplify.configure({
      Auth: {
        Cognito: {
          userPoolId,
          userPoolClientId,
          identityPoolId,
          loginWith: { username: true, email: true },
        },
      },
    });
  } else {
    Amplify.configure({
      Auth: {
        Cognito: {
          userPoolId,
          userPoolClientId,
          loginWith: { username: true, email: true },
        },
      },
    });
  }
  cognitoUserPoolsTokenProvider.setKeyValueStorage(defaultStorage);
  configured = true;
}
