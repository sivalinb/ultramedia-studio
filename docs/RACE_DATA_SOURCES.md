# Race Atlas data notes

The product UI uses a fixed 2016–2025 window so comparisons do not mix partial 2026 data with completed seasons. Canceled editions are preserved as canceled rather than omitted or imputed. Cocodona began in 2021, so the atlas shows every edition available inside the window instead of pretending ten years exist.

## Primary race sources

- UTMB: [official results hub](https://montblanc.utmb.world/en/results). The decade table was cross-checked against the historical UTMB results table, whose yearly references link to official full results.
- Western States: [official results and statistics](https://www.wser.org/results/).
- Hardrock: [official past-results archive](https://www.hardrock100.com/hardrock-pastresults.php), which links to OpenSplitTime result sheets.
- Cocodona: [official Aravaipa results and photos archive](https://www.aravaiparunning.com/cocodona/). Winner detail was cross-checked with iRunFar’s 2022–2025 reports and UltraRunning’s 2021 result listing.

The downloadable product snapshot is `/public/data/race-history-2016-2025.json`. Missing aggregate values remain absent; they are never inferred from a partial leaderboard.

## Photography

UTMB, Western States, and Hardrock images come from Wikimedia Commons and link to their file-description pages, where photographer and license details are maintained. The Cocodona 2025 image is served from iRunFar and links directly to the credited race report. A production commercial release should license contemporary event imagery from each organizer or photographer and store approved derivatives in the product CDN.
