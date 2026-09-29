import { Link } from "react-router-dom";
import { PRIVATE_HOME_PATH } from "@/constants";

export function BillingCancelPage() {
  return (
    <main className="mx-auto flex min-h-svh max-w-md flex-col justify-center bg-[#f4f7f5] px-6">
      <h1 className="text-xl font-bold text-[#0c1f1a]">Checkout canceled</h1>
      <p className="mt-3 text-sm text-[#35584a]">No charge was made. The free allowance is unchanged.</p>
      <Link className="mt-6 text-sm underline text-[#1f7a4d]" to={PRIVATE_HOME_PATH}>
        Back to chat
      </Link>
    </main>
  );
}
