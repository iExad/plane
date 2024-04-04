import { observer } from "mobx-react";
// components
import { GithubOAuthButton, GoogleOAuthButton } from "@/components/account";
// hooks
import { useInstance } from "@/hooks/store";

export const OAuthOptions: React.FC = observer(() => {
  // hooks
  const { instance } = useInstance();

  // derived values
  const areBothOAuthEnabled = instance?.config?.is_google_enabled && instance?.config?.is_github_enabled;

  return (
    <div className="border border-red-500">
      <div className="mx-auto mt-4 flex items-center sm:w-96">
        <hr className="w-full border-onboarding-border-100" />
        <p className="mx-3 flex-shrink-0 text-center text-sm text-onboarding-text-400">Or continue with</p>
        <hr className="w-full border-onboarding-border-100" />
      </div>
      <div className={`mx-auto mt-7 grid gap-4 overflow-hidden sm:w-96 ${areBothOAuthEnabled ? "grid-cols-2" : ""}`}>
        {instance?.config?.is_google_enabled && (
          <div className="flex h-[42px] items-center !overflow-hidden">
            <GoogleOAuthButton text="SignIn with Google" />
          </div>
        )}
        {instance?.config?.is_github_enabled && <GithubOAuthButton text="SignIn with Github" />}
      </div>
    </div>
  );
});