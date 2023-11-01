import { styled, Link as MuiLink } from "@mui/material";

const CopyrightLink = styled(MuiLink) `
  text-decoration: none;
  transition: color 0.3s;
  &:hover {color: ${props => props.theme.palette.secondary[props.theme.palette.mode]}};
` as typeof MuiLink;

export { CopyrightLink };