# Portfolio visual alignment

CSS-only update on branch style/portfolio-alignment.

app.css now imports portfolio-fonts.css, app-base.css and portfolio-theme.css in order. app-base.css preserves the original stylesheet byte for byte. No JavaScript, templates, Python, API, authentication, permissions or monitoring changes. Status/severity variables retain their original values.

Verified in Chromium with the existing live SPA and these exact replacement CSS responses at 320x568, 390x844, 844x390, 1366x768 and 1920x1080: no horizontal overflow, centered login card, reachable card top, 48px inputs, unchanged empty-input validation. Actual authenticated login and dashboard visuals were not tested. Font loading verified. These are isolated browser previews, not a deployment.

Live server still serves original CSS. Repository has a test workflow but no deployment workflow. No SSH configuration or server credentials are available in this workspace. Deploy through the existing self-hosted server process, ensuring all four CSS files are included. No migration is needed. Keep the previous app.css for rollback.
