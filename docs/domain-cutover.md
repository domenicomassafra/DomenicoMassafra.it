# Domain cutover status

Last checked: 2026-10-27 (public DNS, HTTPS, browser and GitHub Pages API).

This file is the operational handoff for the three public domains. It deliberately keeps
registrar, DNS and application deployment as separate steps so a domain change cannot
silently overwrite mail or an existing production origin.

## Current state

| Domain | Registry and DNS observed | Hosting / public HTTPS observed |
|---|---|---|
| `domenicomassafra.it` | `.it` `ok`; `candy.ns.cloudflare.com`, `kanye.ns.cloudflare.com` | GitHub Pages (`domenicomassafra/DomenicoMassafra.it`); apex `200`, `www` `301` to apex |
| `strumentini.it` | `.it` `ok`; same Cloudflare nameservers | Existing Cloudflare Worker deployment; apex `200` |
| `dichiarazionipubbliche.it` | `.it` `ok`; same Cloudflare nameservers | Cloudflare-served application homepage; apex `200`; upstream topology not verified here |

All three apex domains have publicly resolvable `NS` and `A` records. These are
observations from `whois`, `dig` and HTTPS requests on 2026-10-27, not a claim
that each application's deployment or rights checks are complete. DNS delegation
and HTTP application availability are separate states.

## 1. Cloudflare delegation and future repairs

The three domains already resolve using their Cloudflare zones. The original
provisioning sequence was to create one zone per domain:

- `domenicomassafra.it`
- `strumentini.it`
- `dichiarazionipubbliche.it`

The currently observed assigned nameservers for all three are
`candy.ns.cloudflare.com` and `kanye.ns.cloudflare.com`. Always verify the
assigned pair in the zone before any future registrar-side repair.

No registrar or DNS change is required to resolve the current
`domenicomassafra.it` apex or `www` hostname. If delegation changes in the
future, check the `.it` registry status and the actual authoritative records
before changing nameservers.

Do not bulk-copy DNS records between the three zones.

## 2. domenicomassafra.it

GitHub Pages reports `domenicomassafra.it` as the configured custom domain,
`https_enforced: true`, and a workflow build. The production workflow is
`.github/workflows/pages.yml`. On 2026-10-27 the apex returns HTTPS `200`
with `server: GitHub.com`; HTTP apex redirects `301` to HTTPS.

The public apex DNS currently resolves to these GitHub Pages addresses:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

`www.domenicomassafra.it` resolves to Cloudflare proxy addresses (`188.114.96.7`
and `188.114.97.7` in the observed IPv4 answers), so public `dig` cannot
confirm its underlying CNAME target. HTTPS `www` returns `301` to
`https://domenicomassafra.it/`, and both browser requests reach the same
homepage. The live page's `rel=canonical`, `robots.txt` sitemap URL and sitemap
entry all use the HTTPS apex. Do not infer or rewrite the internal Cloudflare
DNS record from public proxy addresses. HTTPS enforcement is already active;
review the actual headers and both hostnames before changing any HSTS policy.

Do not add MX/TXT mail records unless an email provider is intentionally configured.

## 3. strumentini.it

The existing application declares this Cloudflare Worker custom domain in
`../Strumentini.it/wrangler.jsonc`:

```json
{
  "pattern": "strumentini.it",
  "custom_domain": true
}
```

The current checkout is `/Users/domenico/Code/Strumentini.it`. Production is already
active on the apex custom domain; `www.strumentini.it` redirects permanently to the
equivalent apex path. Worker `strumentini` binds `AUTH_DB` to `strumentini-auth`.
The current release has completed live browser smoke plus a real Worker rollback/restore
exercise, and the superseded pre-rebrand D1 resource has been retired.

## 4. dichiarazionipubbliche.it

On 2026-10-27, `https://dichiarazionipubbliche.it/` serves an HTML application
homepage with HTTP `200` through Cloudflare. The previous plan described a
private MiniPC service at `127.0.0.1:18090` behind a future authenticated
Cloudflare Tunnel. That plan is historical; the current upstream/tunnel routing
was not verified by this domain-status check. Do not change its ingress based
on that earlier proposal. The DichiarazioniPubbliche.it repository owns its
release checks, backend verification and public-access decisions.

## 5. Verification

Run:

```sh
./scripts/domain-status.sh
```

For a specific hostname, inspect the status **without** `curl -f` first:

```sh
whois domenicomassafra.it | grep '^Status:'
dig +short NS domenicomassafra.it
dig +short A domenicomassafra.it
dig +short AAAA domenicomassafra.it
dig +short A www.domenicomassafra.it
curl -sSI https://domenicomassafra.it/
curl -sSI https://www.domenicomassafra.it/
```

An HTTP `403` proves an HTTP server responded; it is **not** evidence of DNS
failure. Inspect `Server`, `Location` and any Cloudflare response headers,
compare `GET` with `HEAD` and check the browser before attributing a refusal to
an edge access policy, application authorization or origin. A failed DNS lookup
has no HTTP response. `curl -f` treats an HTTP `403` as a command failure, and
`domain-status.sh` currently reports that situation as `unavailable`; use the
raw HTTP status above when investigating access denials.

For `domenicomassafra.it`, the final gate is:

```sh
curl -fsSIL https://domenicomassafra.it/
curl -fsSIL https://www.domenicomassafra.it/
```

Also open both hostnames in a browser, confirm the final URL is the HTTPS apex,
and inspect the document's `rel=canonical`. On 2026-10-27 both browser requests
reached `https://domenicomassafra.it/` with the expected title and canonical.
This validates domain routing, not the Pages artifact contents: on this date
`/docs/domain-cutover.md` and `/scripts/domain-status.sh` still returned `200`.
Scoping the published artifact belongs to [issue #2](https://github.com/domenicomassafra/DomenicoMassafra.it/issues/2).

For `strumentini.it`, also verify `/robots.txt`, `/sitemap.xml` and
`/api/auth/session` against the intended Cloudflare Worker deployment.

For `dichiarazionipubbliche.it`, an HTTP `200` homepage alone does not establish
the production backend's health, its origin topology, or a completed release.
Verify those in its owning repository before reporting the application cutover
complete.
