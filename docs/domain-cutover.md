# Domain cutover status

Last checked: 2026-10-06.

This file is the operational handoff for the three public domains. It deliberately keeps
registrar, DNS and application deployment as separate steps so a domain change cannot
silently overwrite mail or an existing production origin.

## Current state

| Domain | Registrar state | Intended origin | Ready for traffic? |
|---|---|---|---|
| `domenicomassafra.it` | `inactive / dnsHold` | GitHub Pages, repo `domenicomassafra/DomenicoMassafra.it` | Hosting ready; DNS not delegated |
| `strumentini.it` | `inactive / dnsHold` | Existing Cloudflare Worker `strumentiutili-it` | Source route prepared; production cutover blocked |
| `dichiarazionipubbliche.it` | `inactive / dnsHold` | Existing MiniPC service behind a future public Cloudflare ingress | No public ingress yet |

All three domains were registered at Dynadot on 2026-10-06 and currently return no
authoritative `NS`, `A`, `AAAA`, `MX` or `TXT` records.

## 1. Cloudflare zone creation

Create one Cloudflare Free zone for each apex domain before changing Dynadot nameservers:

- `domenicomassafra.it`
- `strumentini.it`
- `dichiarazionipubbliche.it`

Record the two standard Cloudflare nameservers assigned to each zone. Do not reuse the
nameservers from another zone unless Cloudflare explicitly assigned the same pair.

At Dynadot, replace the domain nameservers with the exact pair Cloudflare assigned for
that domain. `.it` registry DNS validation must pass before the current `dnsHold` clears.

Do not bulk-copy DNS records between the three zones.

## 2. domenicomassafra.it

GitHub Pages is already enabled with `domenicomassafra.it` configured as the custom
domain. The production workflow is `.github/workflows/pages.yml`.

Once the Cloudflare zone exists, add these records initially as **DNS only**:

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
| CNAME | `www` | `domenicomassafra.github.io` |

After public DNS resolves and GitHub has issued the certificate, enable HTTPS enforcement
on GitHub Pages. Keep HSTS off until apex and `www` are both stable.

Do not add MX/TXT mail records unless an email provider is intentionally configured.

## 3. strumentini.it

The existing application already declares this Cloudflare Worker custom domain in
`../StrumentiUtili.it/wrangler.jsonc`:

```json
{
  "pattern": "strumentini.it",
  "custom_domain": true
}
```

The current checkout of `StrumentiUtili.it` is not a safe deployment source because it
contains a very large uncommitted WIP. Do **not** run `wrangler deploy` from that checkout.

After the Cloudflare zone is active:

1. create a clean, reviewed deployment checkout/worktree from the intended release commit;
2. run the repository release gates there;
3. deploy the existing Worker so the `custom_domain` attachment creates the apex route;
4. configure `www.strumentini.it` as a proxied hostname plus a permanent redirect to the
   same path on `https://strumentini.it`;
5. preserve the legacy `strumentiutili.it` deployment until Strumentini smoke tests pass.

The Worker name and D1 database remain `strumentiutili-it` and `strumentiutili-auth`; they
are infrastructure identifiers and are not renamed by the public-domain cutover.

## 4. dichiarazionipubbliche.it

The repository currently has no public ingress. Its service is bound to
`127.0.0.1:18090` on the MiniPC and the existing HTTPS preview is tailnet-only.

It is safe to add and delegate the Cloudflare zone now, but do not create an apex/`www`
origin record until the public ingress is explicit and tested. The preferred topology is:

`Cloudflare edge -> authenticated Cloudflare Tunnel on MiniPC -> 127.0.0.1:18090`

This keeps the MiniPC port closed to the public Internet. Before attaching the hostname,
build `web/dist` from the approved production projection and run the repository's public
release checks.

## 5. Verification

Run:

```sh
./scripts/domain-status.sh
```

For `domenicomassafra.it`, the final gate is:

```sh
curl -fsSIL https://domenicomassafra.it/
curl -fsSIL https://www.domenicomassafra.it/
```

For `strumentini.it`, also verify `/robots.txt`, `/sitemap.xml` and
`/api/auth/session` against the intended Cloudflare Worker deployment.

For `dichiarazionipubbliche.it`, do not call the public cutover complete until the public
health endpoint and representative public pages are served through the chosen Cloudflare
ingress without exposing the origin port directly.
