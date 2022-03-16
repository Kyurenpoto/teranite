<script lang="ts">
  import ArtistsSection from "../components/ArtistsSection.svelte";
  import DiscoverySection from "../components/DiscoverySection.svelte";
  import MainSection from "../components/MainSection.svelte";
  import RecentSection from "../components/RecentSection.svelte";
  import { hasAccount } from "../stores/hasAccount";
</script>

{#if $hasAccount === true}
  <MainSection>
    <RecentSection />
    <ArtistsSection />
    <DiscoverySection />
  </MainSection>
{/if}
