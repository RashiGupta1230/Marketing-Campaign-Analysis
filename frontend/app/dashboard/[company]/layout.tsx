import { Sidebar } from "@/components/dashboard/Sidebar";
import { ErrorBoundary } from "@/components/ErrorBoundary";

interface DashboardLayoutProps {
  children: React.ReactNode;
  params: { company: string };
}

export default function DashboardLayout({ children, params }: DashboardLayoutProps) {
  const companyName = params.company
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar company={params.company} companyName={companyName} />
      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        <ErrorBoundary>{children}</ErrorBoundary>
      </div>
    </div>
  );
}
