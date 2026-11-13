
"use client";

import { useActivate } from "@/lib/query/use-auth";
import { useRouter } from "next/navigation";
import React, { use, useEffect, useRef } from "react";
import { toast } from "react-toastify";

interface ActivationProps {
  params: Promise<{
    uid: string;
    token: string;
  }>;
}

export default function ActivationPage({ params }: ActivationProps) {
  const { uid, token } = use(params);
  const router = useRouter();

  const activate = useActivate();
  const hasFired = useRef(false);

  // Fire the mutation once on mount.
  useEffect(() => {
    if (hasFired.current) return;
    hasFired.current = true;
    activate.mutate({ uid, token });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (activate.isSuccess) {
      toast.success("Account successfully activated!");
      router.push("/login");
    } else if (activate.isError) {
      console.error("Activation error:", JSON.stringify(activate.error, null, 2));
      toast.error("Failed to activate your account.");
    }
  }, [activate.isSuccess, activate.isError, activate.error, router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h3 className="dark:text-platinum text-2xl font-robotoSlab font-bold text-gray-800 sm:text-4xl md:text-5xl">
          {activate.isPending ? (
            <div className="flex-center">
              <span className="mr-2">⏰</span>
              <span>Activating your account .... please wait.</span>
              <span className="ml-2">🥱</span>
            </div>
          ) : activate.isSuccess ? (
            <div className="flex-center">
              <span className="mr-2">✅</span>
              <span>Account activated successfully!</span>
            </div>
          ) : activate.isError ? (
            <div className="flex-center">
              <span className="mr-2">❌</span>
              <span>Your account has already been activated....</span>
            </div>
          ) : null}
        </h3>
      </div>
    </div>
  );
}