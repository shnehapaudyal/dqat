export const snakeCaseToTitleCase = (str) => {
  return str
    ?.split("_")
    .filter((x) => x.length > 0)
    .map((x) => x.charAt(0).toUpperCase() + x.slice(1))
    .join(" ");
};

// export const camelCaseToTitleCase = (str) => str.replace(/(?:^|\s)\w/g, (match) => match.toUpperCase());
export const camelCaseToTitleCase = (str) => str.replace(/([A-Z])/g, ' $1').trim().toLowerCase().replace(/^./, (match) => match.toUpperCase());