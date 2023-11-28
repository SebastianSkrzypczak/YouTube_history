function secondsToDhms(seconds) {
    const days = Math.floor(seconds / (3600 * 24));
    const hours = Math.floor((seconds % (3600 * 24)) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${days}D:${hours}H:${minutes}M:${remainingSeconds}S`;
}

export default secondsToDhms;