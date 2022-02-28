<script lang="ts">
  import BasePage from "../components/BasePage.svelte";
  import NavBar from "../components/NavBar.svelte";
  import MainSection from "../components/MainSection.svelte";
  import RecentSection from "../components/RecentSection.svelte";
  import ArtistsSection from "../components/ArtistsSection.svelte";
  import DiscoverySection from "../components/DiscoverySection.svelte";
  import InfoNavBar from "../components/InfoNavBar.svelte";
  import { hasAccount } from "../stores";
</script>

<BasePage class="bg-[#242424]">
  <NavBar class="bg-blue-900" />
  <MainSection>
    {#if $hasAccount == true}
      <RecentSection />
      <ArtistsSection />
      <DiscoverySection />
    {:else}
      <div></div>
    {/if}
  </MainSection>
  <InfoNavBar class="bg-blue-900" />
</BasePage>
