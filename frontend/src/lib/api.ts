import {
  ResearchRequest,
  ResearchResponse,
} from "@/lib/types";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";


export async function researchCompany(
  request: ResearchRequest,
): Promise<ResearchResponse> {
  const response = await fetch(
    `${API_URL}/api/research`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(request),
    },
  );

  if (!response.ok) {
    let message =
      "Company research failed.";

    try {
      const error = await response.json();

      if (error.detail) {
        message = error.detail;
      }
    } catch {
      // Keep generic message.
    }

    throw new Error(message);
  }

  return response.json();
}


export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(
      `${API_URL}/api/health`,
      {
        cache: "no-store",
      },
    );

    return response.ok;
  } catch {
    return false;
  }
}