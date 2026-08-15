import {
  ResearchRequest,
  ResearchJobCreated,
  ResearchJobResultResponse,
  ResearchJobStatusResponse,
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

export async function createResearchJob(
  request: ResearchRequest,
): Promise<ResearchJobCreated> {
  const response = await fetch(
    `${API_URL}/api/research/jobs`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(
        request,
      ),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(
        response,
        "Failed to start research.",
      ),
    );
  }

  return response.json();
}


export async function getResearchJobStatus(
  jobId: string,
): Promise<ResearchJobStatusResponse> {
  const response = await fetch(
    `${API_URL}/api/research/jobs/${jobId}`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(
        response,
        "Failed to retrieve research status.",
      ),
    );
  }

  return response.json();
}


export async function getResearchJobResult(
  jobId: string,
): Promise<ResearchJobResultResponse> {
  const response = await fetch(
    `${API_URL}/api/research/jobs/${jobId}/result`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(
        response,
        "Failed to retrieve research result.",
      ),
    );
  }

  return response.json();
}


async function getErrorMessage(
  response: Response,
  fallback: string,
): Promise<string> {
  try {
    const data =
      await response.json();

    if (
      typeof data.detail
      === "string"
    ) {
      return data.detail;
    }
  } catch {
    // Ignore malformed error body.
  }

  return fallback;
}