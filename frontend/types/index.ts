export type Role = "admin" | "analyst" | "viewer";
export type PlanTier = "starter" | "pro" | "enterprise";
export type ReportStatus = "draft" | "signed_off";

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  avatarInitials?: string;
  createdAt: string;
}

export interface Company {
  id: string;
  name: string;
  slug: string;
  industry: string;
  plan: PlanTier;
  memberCount: number;
  createdAt: string;
}

export interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: Role;
  status: "active" | "pending";
  lastActive?: string;
}

export interface KPIData {
  spend: number;
  revenue: number;
  conversions: number;
  roas: number;
  roiPercent: number;
  cac: number;
  ltvCac: number;
  paybackMonths: number;
}

export interface ChannelMetric {
  channel: string;
  spend: number;
  attributedRevenue: number;
  roas: number;
  conversions: number;
  weight: number;
}

export interface AttributionResult {
  model: string;
  totalSpend: number;
  totalRevenue: number;
  totalAttributedRevenue: number;
  blendedRoas: number;
  channels: ChannelMetric[];
  revenueConserved: boolean;
}

export interface OptimizerChannel {
  channel: string;
  baseSpend: number;
  optimizedSpend: number;
  delta: number;
  deltaPct: number;
  projectedRoas: number;
  marginalRoas: number;
  revenueImpact: number;
  profitImpact: number;
}

export interface OptimizerResult {
  targetBudget: number;
  objective: string;
  projectedTotalRevenue: number;
  projectedBlendedRoas: number;
  channels: OptimizerChannel[];
  aiRecommendation: { title: string; impact: string; body: string };
}

export interface Report {
  id: string;
  title: string;
  scenario: string;
  attributionModel: string;
  dateRange: [string, string];
  status: ReportStatus;
  createdBy: string;
  createdAt: string;
  auditId?: string;
}

export interface AuditRecord {
  auditId: string;
  timestamp: string;
  scenario: string;
  approvedBy: string;
  targetBudget: number;
  projectedRoas: number;
  verificationHash: string;
}
