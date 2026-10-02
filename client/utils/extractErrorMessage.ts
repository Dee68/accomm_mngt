export default function extractErrorMessage(error: unknown): string | null {
  if (
    typeof error === "object" &&
    error !== null &&
    "data" in error
  ) {
    const errorData = (error as { data: any }).data;

    // ✅ Guard: errorData must be a plain object before we use `in` / Object.keys
    if (typeof errorData === "string") {
      // Backend returned HTML (e.g. Django debug page) or plain text
      return null; // or "Server error. Please try again." if you prefer
    }

    if (
      typeof errorData === "object" &&
      errorData !== null &&
      "detail" in errorData &&
      typeof errorData.detail === "string"
    ) {
      return errorData.detail;
    }

    if (typeof errorData !== "object" || errorData === null) {
      return null;
    }

    const messages: string[] = [];
    Object.keys(errorData).forEach((key) => {
      if (key !== "status_code") {
        const fieldError = errorData[key];
        if (Array.isArray(fieldError)) {
          messages.push(...fieldError);
        } else if (typeof fieldError === "object" && fieldError !== null) {
          Object.values(fieldError).forEach((errorMessages: any) => {
            if (Array.isArray(errorMessages)) {
              messages.push(...errorMessages);
            }
          });
        }
      }
    });

    return messages.length > 0 ? messages.join(", ") : null;
  }
  return null;
}

