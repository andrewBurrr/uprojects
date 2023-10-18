import { styled, Grid } from "@mui/material";

const FormGridContainer = styled(Grid) `
  flex: 1;
  color: ${props => props.theme.palette.grey[200]};
  display: flex;
  justify-content: center;
  align-items: center;
` as typeof Grid;

export { FormGridContainer };