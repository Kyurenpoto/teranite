<script lang="ts">
  import { afterUpdate } from "svelte";
  import { baseUrl } from "../modules/baseUrl";

  let social_type = window.location.pathname.split("/")[2];

  afterUpdate(async () => {
    try {
      let response = await fetch(`${baseUrl}/token/${social_type}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: new URL(window.location.href).searchParams.get("code") }),
      });
      let json = await response.json();

      localStorage.hasAccount = json["has_account"];
      localStorage.accessToken = json["access_token"];
      localStorage.refreshToken = json["refresh_token"];

      history.replaceState({}, "", "/");
    } catch (error) {
      console.error(error);
    }
  });
</script>

<div class="min-h-screen w-[calc(100vw-var(--scrollbar-width))] grid items-center justify-center bg-fuchsia-700">
  <p>Redirect to Github..</p>
</div>
