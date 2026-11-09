
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type RewritePreferences = {
  tone: string;
  length: string;
  recipient: string;
};

type RewriteResponse = {
  rewritten_message: string;
};

export async function rewriteMessage(
  message: string,
  preferences: RewritePreferences,
): Promise<string> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}/api/rewrite`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        ...preferences,
      }),
    });
  } catch {
    throw new Error(
      "Unable to connect to the server. Please check whether the backend is running.",
    );
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    const detail = errorData?.detail;

    if (response.status === 422) {
      throw new Error(
        "The message or preferences are invalid. Please check your inputs.",
      );
    }

    if (response.status === 400) {
      throw new Error(
        typeof detail === "string"
          ? detail
          : "The message could not be rewritten with these inputs.",
      );
    }

    if (response.status === 502 || response.status === 503) {
      throw new Error(
        "The rewriting service is temporarily unavailable. Please try again.",
      );
    }

    throw new Error("Something went wrong. Please try again.");
  }

  const data: RewriteResponse = await response.json();
  return data.rewritten_message;
}
