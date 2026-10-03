/**
 * CareerLens AI - Frontend API Client Pattern
 *
 * Simplified public portfolio example showing how the frontend
 * communicates with protected backend endpoints.
 *
 * The production API client includes additional authentication,
 * refresh, timeout, and error-handling behavior.
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface RequestOptions extends RequestInit {
  accessToken?: string;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {},
): Promise<T> {
  const { accessToken, headers, ...requestOptions } = options;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...requestOptions,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken
        ? { Authorization: `Bearer ${accessToken}` }
        : {}),
      ...headers,
    },
  });

  if (!response.ok) {
    let message = "Request failed";

    try {
      const errorBody = await response.json();

      if (typeof errorBody.detail === "string") {
        message = errorBody.detail;
      }
    } catch {
      // Keep the generic error message when no JSON body is available.
    }

    throw new ApiError(response.status, message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}


export interface ResumeSummary {
  id: number;
  original_filename: string;
  file_type: string;
  created_at: string;
}


export function getResumes(
  accessToken: string,
): Promise<ResumeSummary[]> {
  return apiRequest<ResumeSummary[]>("/resumes", {
    method: "GET",
    accessToken,
  });
}