export function formatPercent(
  value: number | null | undefined,
  digits = 1,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return `${(value * 100).toFixed(
    digits,
  )}%`;
}


export function formatNumber(
  value: number | null | undefined,
  digits = 2,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return value.toFixed(
    digits,
  );
}


export function formatCurrency(
  value: number | null | undefined,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return new Intl.NumberFormat(
    "en-US",
    {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 2,
    },
  ).format(value);
}


export function formatCompactCurrency(
  value: number | null | undefined,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return new Intl.NumberFormat(
    "en-US",
    {
      style: "currency",
      currency: "USD",

      notation: "compact",

      maximumFractionDigits: 2,
    },
  ).format(value);
}


export function formatLabel(
  value: string,
): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase(),
    );
}