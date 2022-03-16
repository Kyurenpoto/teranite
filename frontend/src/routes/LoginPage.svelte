<script lang="ts">
  import { beforeUpdate } from "svelte";

  import { baseUrl } from "../modules/urlUtils";
  import { hasAccount } from "../stores/hasAccount";

  const clientId = "Iv1.886232f678ac9a33";
  const redirectUri = `${baseUrl}/login/github/callback`;

  beforeUpdate(async () => {
    if ($hasAccount === true) {
      history.replaceState({}, "", "/");

      window.dispatchEvent(new Event("update-page"));
    }
  });
</script>

<section class="w-full h-[calc(100vh-240px)] my-10 flex flex-col gap-y-10 items-center justify-center bg-fuchsia-700">
  <div class="w-[var(--grid-column-2)] h-20 grid place-items-center bg-red-500">Sign In</div>
  <a
    class="w-[var(--grid-column-4)] h-[60px] grid place-items-center bg-red-500"
    href="https://github.com/login/oauth/authorize?client_id={clientId}&redirect_uri={redirectUri}"
  >
    Github
  </a>
</section>
