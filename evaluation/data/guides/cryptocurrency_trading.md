# Cryptocurrency Trading Analytics (CryptoExchange Database)

The digital assets division follows these strict conventions for crypto data analysis:

## Price Calculations

- Always use the volume-weighted average price (VWAP) for daily price reporting, never simple close price.
- Prices must be denominated in USD unless explicitly requested in another currency pair.
- "Stale" price data (no trades for >4 hours on a 24/7 market) should be flagged and excluded from real-time dashboards.
- Price differences > 5% between exchanges for the same asset indicate potential arbitrage or data quality issues - flag these.
- Flash crashes (price drops > 20% within 5 minutes that recover within 1 hour) should be excluded from volatility calculations.

## Token Classification

- Layer 1 tokens (BTC, ETH, SOL, etc.) are analyzed separately from Layer 2 and application tokens.
- Stablecoins (USDT, USDC, DAI, etc.) must be EXCLUDED from market cap rankings and price performance metrics.
- Tokens with market cap below $10M are "micro-caps" and should carry a data reliability warning.
- Wrapped tokens (wBTC, wETH) are NOT the same as their native versions for volume analysis - track separately.
- Governance tokens should be flagged and their circulating supply adjusted for locked/staked amounts.

## Volume Metrics

- "Wash trading" detection: exclude any trading pair where buy and sell volumes match within 0.1% over a 24-hour period.
- Only count trades on exchanges with proof-of-reserves certification for "verified volume" metrics.
- OTC (over-the-counter) trades are NOT included in exchange volume - they are reported separately if available.
- NFT transaction volume is tracked in a completely separate pipeline - never combine with fungible token metrics.
- Volume spikes > 10x the 30-day average should trigger a data quality review before inclusion in reports.

## Wallet Analysis

- Wallets holding > 1% of a token's total supply are "whale wallets" and their transactions must be flagged.
- Exchange wallets (hot and cold) should be excluded from "holder distribution" analysis.
- Smart contract addresses are NOT user wallets - filter these from active address counts.
- Dust transactions (value < $0.01) should be excluded from transaction count metrics.
- Multi-signature wallets count as a single entity regardless of the number of signers.

## Regulatory Compliance

- Transactions originating from OFAC-sanctioned addresses must be flagged and excluded from standard reporting.
- KYC-verified volume should be tracked separately from anonymous/pseudonymous volume.
- Tax lot calculations use FIFO (First In, First Out) unless the user specifies LIFO or specific identification.
- Cross-border transactions must include jurisdiction tagging for regulatory reporting.
- DeFi protocol interactions (swaps, lending, staking) generate taxable events - track cost basis accordingly.

## Time Series Conventions

- Cryptocurrency markets operate 24/7/365 - there is no "market close" or "trading session."
- Use UTC timestamps exclusively for all cross-exchange comparisons.
- Hourly candles are the standard granularity for intra-day analysis; daily for trend analysis.
- Blockchain timestamps may differ from exchange timestamps by up to 15 minutes - use exchange time for trade analysis.
- Halving events and hard forks require special period markers in all time series.
