<script lang="ts">
  import MainSection from "../components/MainSection.svelte";
  import RecentSection from "../components/RecentSection.svelte";
  import ArtistsSection from "../components/ArtistsSection.svelte";
  import DiscoverySection from "../components/DiscoverySection.svelte";
  import { hasAccount } from "../stores";
</script>

{#if $hasAccount == true}
  <MainSection>
    <RecentSection />
    <ArtistsSection />
    <DiscoverySection />
  </MainSection>
{/if}
