export type InvestmentRecommendation =
  | "strongly_attractive"
  | "attractive"
  | "watchlist"
  | "neutral"
  | "unattractive"
  | "strongly_unattractive"
  | "insufficient_data";

export type ConvictionLevel =
  | "low"
  | "moderate"
  | "high";

export type InvestmentHorizon =
  | "short_term"
  | "medium_term"
  | "long_term";

export interface ResearchRequest {
  ticker: string;
  fiscal_year: number;
  market_years: number;

  benchmark_ticker: string;

  risk_free_rate_annual: number;

  news_query: string;
  news_limit: number;

  refresh_market: boolean;
  refresh_fundamentals: boolean;
}

export interface CommitteeEvidence {
  source_type:
    | "market_metric"
    | "fundamental_metric"
    | "valuation_metric"
    | "risk_metric"
    | "news_event";

  field: string;

  source_id: string | null;

  interpretation: string;
}

export interface InvestmentCommittee {
  ticker: string;

  recommendation: InvestmentRecommendation;

  conviction: ConvictionLevel;

  confidence_score: number;

  investment_horizon: InvestmentHorizon;

  thesis: string;

  bull_case: string;
  bear_case: string;

  market_view: string;
  fundamental_view: string;
  valuation_view: string;
  risk_view: string;
  news_view: string;

  key_catalysts: string[];
  key_risks: string[];

  evidence: CommitteeEvidence[];

  conditions_to_upgrade: string[];
  conditions_to_downgrade: string[];

  limitations: string[];

  final_summary: string;
}

export interface MarketMetrics {
  ticker: string;

  latest_close: number;

  total_return: number | null;
  annualized_return: number | null;
  annualized_volatility: number | null;

  maximum_drawdown: number | null;

  return_1_month: number | null;
  return_3_months: number | null;
  return_6_months: number | null;
  return_1_year: number | null;

  trend: string;
}

export interface FundamentalMetrics {
  ticker: string;
  fiscal_year: number;

  revenue: number | null;
  net_income: number | null;

  free_cash_flow: number | null;

  revenue_growth: number | null;
  net_income_growth: number | null;

  operating_margin: number | null;
  net_margin: number | null;

  return_on_equity: number | null;
}

export interface ValuationMetrics {
  ticker: string;

  share_price: number;

  market_cap: number | null;

  enterprise_value: number | null;

  trailing_pe: number | null;

  earnings_yield: number | null;

  price_to_sales: number | null;
  price_to_book: number | null;

  ev_to_sales: number | null;

  free_cash_flow_yield: number | null;
}

export interface RiskMetrics {
  ticker: string;

  annualized_volatility: number | null;

  beta: number | null;

  sharpe_ratio: number | null;
  sortino_ratio: number | null;

  daily_var_95: number | null;
  daily_cvar_95: number | null;

  maximum_drawdown: number | null;
}

export interface ResearchBundle {
  ticker: string;

  market_metrics: MarketMetrics;

  fundamental_metrics: FundamentalMetrics;

  valuation_metrics: ValuationMetrics;

  risk_metrics: RiskMetrics;
}

export interface CompanyInvestmentReport {
  ticker: string;

  generated_at: string;

  research: ResearchBundle;

  committee: InvestmentCommittee;
}

export interface ResearchResponse {
  report: CompanyInvestmentReport;
}

export type ResearchJobStatus =
  | "queued"
  | "running"
  | "completed"
  | "failed";


export type ResearchStepStatus =
  | "waiting"
  | "running"
  | "completed"
  | "failed";


export interface ResearchStep {
  name: string;

  label: string;

  status: ResearchStepStatus;
}


export interface ResearchJobCreated {
  job_id: string;

  status: ResearchJobStatus;
}


export interface ResearchJobStatusResponse {
  job_id: string;

  ticker: string;

  status: ResearchJobStatus;

  current_step: string | null;

  progress: number;

  steps: ResearchStep[];

  error: string | null;
}


export interface ResearchJobResultResponse {
  job_id: string;

  report: CompanyInvestmentReport;
}