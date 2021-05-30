import React, { useState } from "react"
import Button from "@material-ui/core/Button"
import Grid from "@material-ui/core/Grid"
import Typography from "@material-ui/core/Typography"
import TextField from "@material-ui/core/TextField"
import FormControl from "@material-ui/core/FormControl"
import FormHelperText from "@material-ui/core/FormHelperText"
import Radio from "@material-ui/core/Radio"
import RadioGroup from "@material-ui/core/RadioGroup"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import { Link } from "react-router-dom"


function CreateRoomPage() {

  const [guestCatPause, setGuestCanPause] = useState(true);
  const [votesToSkip, setVotesToSkip] = useState(1);

  const handleGuestCanPause = (e) => setGuestCanPause(e.target.value === 'true')
  const handleVotesToSkip = (e) => setVotesToSkip(parseInt(e.target.value))
  const handleSubmit = async (e) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guest_can_pause: guestCatPause, votes_to_skip: votesToSkip })
    }
    const response = await (await fetch('/api/create-room', requestOptions)).json()
    console.log(response)
  }

  return (
    <Grid container spacing={1}>
      {/* Heading */}
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">Create a New Room</Typography>
      </Grid>
      {/* guest_can_pause */}
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText component="span">
            <div align='center'>Guest control of playback state</div>
            <RadioGroup row defaultValue="true" onChange={handleGuestCanPause}>
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormHelperText>
        </FormControl>
      </Grid>
      {/* votes_to_skip */}
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            defaultValue={1}
            inputProps={{ min: 1, style: { textAlign: "center" } }}
            onChange={handleVotesToSkip}
          />
          <FormHelperText component="span">
            <div align="center">Votes required to skip</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      {/* Submit */}
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" onClick={handleSubmit}>
          Create A Room
        </Button>
      </Grid>
      {/* Back */}
      <Grid item xs={12} align="center">
        <Button color="primary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  )
}

export default CreateRoomPage
