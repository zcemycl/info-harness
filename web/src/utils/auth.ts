import { confirmSignIn, signIn, type ConfirmSignInInput, type SignInInput, type SignInOutput } from "aws-amplify/auth";

export async function amplifySignIn(input: SignInInput): Promise<SignInOutput> {
  return signIn(input);
}

export async function amplifyConfirmSignIn(input: ConfirmSignInInput): Promise<SignInOutput> {
  return confirmSignIn(input);
}
