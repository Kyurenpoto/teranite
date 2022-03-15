<script lang="ts">
  import { afterUpdate } from "svelte";

  import { baseUrl } from "../modules/urlUtils";
  import { hasAccount } from "../stores/hasAccount";

  const validTokenTypes = ["github"];

  afterUpdate(async () => {
    if ($hasAccount === true) {
      history.replaceState({}, "", "/");

      window.dispatchEvent(new Event("update-page"));
    }

    try {
      const tokenType = window.location.pathname.split("/")[2];
      if (!validTokenTypes.includes(tokenType)) {
        return;
      }

      const response = await fetch(`${baseUrl}/token/${tokenType}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: new URL(window.location.href).searchParams.get("code") }),
      });
      const json = await response.json();

      $hasAccount = JSON.parse(json.has_account);
      localStorage.accessToken = json.access_token;
      localStorage.refreshToken = json.refresh_token;
    } catch (error) {
      console.error(error);
    } finally {
      history.replaceState({}, "", "/");

      window.dispatchEvent(new Event("update-page"));
    }
  });
</script>

<div class="w-full min-h-screen grid items-center justify-center bg-fuchsia-700">
  <p>Redirect to Github..</p>
</div>
