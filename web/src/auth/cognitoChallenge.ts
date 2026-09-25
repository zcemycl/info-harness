export type CognitoChallengeStep =
  | "DONE"
  | "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED"
  | "CONFIRM_SIGN_IN_WITH_SMS_CODE"
  | "CONFIRM_SIGN_IN_WITH_TOTP_CODE"
  | "CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE"
  | "CONFIRM_SIGN_IN_WITH_EMAIL_CODE"
  | "OTHER";

const SIGN_IN_STATE_PREFIX = "CognitoSignInState";

export function mapSignInStep(nextStep?: string): CognitoChallengeStep {
  switch (nextStep) {
    case "DONE":
      return "DONE";
    case "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED":
      return "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED";
    case "CONFIRM_SIGN_IN_WITH_SMS_CODE":
      return "CONFIRM_SIGN_IN_WITH_SMS_CODE";
    case "CONFIRM_SIGN_IN_WITH_TOTP_CODE":
      return "CONFIRM_SIGN_IN_WITH_TOTP_CODE";
    case "CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE":
      return "CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE";
    case "CONFIRM_SIGN_IN_WITH_EMAIL_CODE":
      return "CONFIRM_SIGN_IN_WITH_EMAIL_CODE";
    default:
      return "OTHER";
  }
}

export function mapChallengeName(challengeName: string): CognitoChallengeStep {
  switch (challengeName) {
    case "NEW_PASSWORD_REQUIRED":
      return "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED";
    case "SMS_MFA":
    case "SMS_OTP":
      return "CONFIRM_SIGN_IN_WITH_SMS_CODE";
    case "SOFTWARE_TOKEN_MFA":
      return "CONFIRM_SIGN_IN_WITH_TOTP_CODE";
    case "EMAIL_OTP":
      return "CONFIRM_SIGN_IN_WITH_EMAIL_CODE";
    case "CUSTOM_CHALLENGE":
      return "CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE";
    default:
      return "OTHER";
  }
}

export function getPendingSignInChallenge(): CognitoChallengeStep | null {
  const expiry = sessionStorage.getItem(`${SIGN_IN_STATE_PREFIX}.expiry`);
  if (!expiry || Number(expiry) <= Date.now()) return null;
  const challengeName = sessionStorage.getItem(`${SIGN_IN_STATE_PREFIX}.challengeName`);
  const signInSession = sessionStorage.getItem(`${SIGN_IN_STATE_PREFIX}.signInSession`);
  if (!challengeName || !signInSession) return null;
  const step = mapChallengeName(challengeName);
  return step === "OTHER" ? null : step;
}
