import {
  ResearchProgress,
} from "@/components/research/research-progress";


export default async function ResearchJobPage({
  params,
}: {
  params: Promise<{
    jobId: string;
  }>;
}) {
  const {
    jobId,
  } = await params;

  return (
    <ResearchProgress
      jobId={jobId}
    />
  );
}