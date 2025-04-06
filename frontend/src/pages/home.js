import { useEffect, useState } from "react";
import { fetchHome } from "../api";

const Home = () => {
  return (
    <div>
      <div className="home_page_body" id="edit_partition">
        <div>
          <h1>New Partition</h1>
        </div>
      </div>

      <div class="home_page_body" id="partition_info">
        <div>
          <h1>My Saved Partitions</h1>
        </div>
      </div>

      <div class="home_page_body" id="tracks">
        <div>
          <h1>User tracks</h1>
        </div>
      </div>
    </div>
  );
};

export default Home;
